# -*- coding: utf-8 -*-
"""
The Clue Coach, server side. app.py calls judge() when you press "check my answer" in Mock OA.

What happens on one call:
  1. key_for(question)   turns the question's own fields (its variant, its accepted alternatives, its core,
                         its tell, its clue phrases, its decoys, its glossary) into the CONFIDENTIAL KEY.
                         Nothing is solved here: the answer was written when the question was written, so
                         the model is comparing, not solving.
  2. _ask()              sends the story, the key and your typed answer to the model. If the chosen model is
                         down or slow (providers do go down), it walks the fallback chain in llm_config.
  3. leak_check()        reads the reply back. If it names the approach, quotes the story, echoes the key's
                         own core/tell, or plainly hands the answer over, the reply is thrown out, the model
                         is asked once more with a warning, and if it leaks again a canned nudge written here
                         is sent instead. The verdict survives either way: one word cannot leak anything.

The API key is read from .env by llm_config and used here, on the server. It never reaches the browser.
"""
import json, os, re, sys, time, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import aliases
import tasks
import llm_config
import pattern_library as PL
from llm_check import call
from llm_prompts import JUDGE_PROMPT, TEACH_PROMPT, build_judge_message, build_teach_message

VNAME = {v["id"]: v["name"] for p in PL.PATTERNS for v in p["variants"]}
PNAME = {p["id"]: p["name"] for p in PL.PATTERNS}
VPAT = {v["id"]: p["id"] for p in PL.PATTERNS for v in p["variants"]}

VERDICTS = ("right", "close", "wrong", "unclear")

# Said plainly enough to count as handing the answer over, whatever words surround it.
GIVES_AWAY = re.compile(r"(the answer is|correct answer|the correct (pattern|approach|variant|technique)|"
                        r"you should use|you need to use|it is actually|it's actually|the pattern is|"
                        r"the approach is|the technique is|what you want here is|the right answer)", re.I)

# The deciding word is usually the whole answer, so the coach may not supply one the student has not used.
DECIDERS = ("longest", "shortest", "smallest", "largest", "biggest", "maximum", "minimum", "fewest", "most",
            "cheapest", "nearest", "peak", "unbroken", "consecutive", "contiguous", "adjacent", "distinct",
            "overlapping", "simultaneous", "exactly")


# --------------------------------------------------------------------------------------------------
#  Building the key from a question
# --------------------------------------------------------------------------------------------------
def _sentences(story):
    """Split a story into sentences, keeping a paragraph/sentence label for each."""
    out = []
    for pi, para in enumerate(p for p in story.split("\n") if p.strip()):
        for si, sent in enumerate(re.split(r"(?<=[.?!])\s+", para.strip())):
            label = "sentence %d" % (si + 1) if pi == 0 else "paragraph %d, sentence %d" % (pi + 1, si + 1)
            out.append((label, sent))
    return out


def _where(story, phrase):
    for label, sentence in _sentences(story):
        if phrase in sentence:
            return label
    return "somewhere in the story"


def forbidden_for(vid):
    """Every name and phrasing that would hand over this variant, plus its pattern's own names."""
    pid = VPAT[vid]
    terms = {VNAME[vid], PNAME[pid]}
    terms.update(aliases.PATTERN.get(pid, []))
    terms.update(aliases.VARIANT.get(vid, []))
    # drop the short terms that are ordinary English and would block honest sentences
    skip = {"dict", "bits", "prune", "board", "maze", "span", "cut", "sort by", "events"}
    keep = [t for t in terms if len(t) > 3 and t.lower() not in skip]
    return sorted(keep, key=lambda t: (-len(t), t))


def shown_story(q):
    """Exactly what the student sees: the story, then the task line and the sample test."""
    t = tasks.TASKS.get(q["id"])
    if not t:
        return q["story"]
    nl = chr(10)
    return (q["story"] + nl * 2 + "YOUR TASK (shown to the student): " + t[0] + nl * 2 +
            "SAMPLE INPUT (shown to the student):" + nl + t[1] + nl +
            "SAMPLE OUTPUT (shown to the student):" + nl + t[2] + nl +
            "SAMPLE EXPLANATION: " + t[3])


def key_for(q):
    """The CONFIDENTIAL KEY for one question dict from sc_check.load()."""
    vid, story = q["v"], q["story"]
    return {
        "approach": "%s  -  %s" % (PNAME[VPAT[vid]], VNAME[vid]),
        "alternatives": ["%s - %s" % (PNAME[VPAT[a]], VNAME[a]) for a in q.get("alt", [])],
        "core": q.get("core", ""),
        "tell": q.get("tell", ""),
        "forbidden": forbidden_for(vid),
        "clues": [{"where": "%s holds a clue (never quote it; its words are: %s)" % (_where(story, c), c),
                   "signals": q.get("tell", "")} for c in q.get("clues", [])],
        "decoys": list(q.get("decoys", [])),
        "glossary": [{"word": g[0], "meaning": g[1], "safe": bool(g[2])} for g in q.get("gloss", [])],
        "clue_phrases": list(q.get("clues", [])),
        "story": story,
    }


# --------------------------------------------------------------------------------------------------
#  Reading the reply back: a prompt is never a guarantee, so every reply is checked
# --------------------------------------------------------------------------------------------------
def _norm(s):
    return " " + re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip() + " "


def _runs(text, n=6):
    w = _norm(text).split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def leak_check(reply, key, student_text):
    """Return the reasons this reply must not be shown. An empty list means it is safe."""
    low = _norm(reply)
    mine = _norm(student_text)          # whatever the student said themselves is theirs to hear back
    bad = []

    for t in key["forbidden"]:
        nt = _norm(t).strip()
        if nt and (" " + nt + " ") in low and (" " + nt + " ") not in mine:
            bad.append("named the approach (" + t + ")")
            break

    for p in key["clue_phrases"]:
        w = _norm(p).split()
        if len(w) >= 4 and " ".join(w[:4]) in low:
            bad.append("quoted a clue phrase")
            break

    if not bad:                         # any four words lifted straight out of the story
        story_runs = _runs(key.get("story", ""), 4)
        lifted = (_runs(reply, 4) & story_runs) - _runs(student_text, 4)
        if lifted:
            bad.append("quoted the story (" + sorted(lifted)[0] + ")")

    echo = _runs(reply) & (_runs(key.get("core", "")) | _runs(key.get("tell", "")))
    if echo:
        bad.append("echoed the key (" + sorted(echo)[0] + ")")

    supplied = [w for w in DECIDERS if (" " + w + " ") in low and (" " + w + " ") not in mine]
    if supplied:
        bad.append("supplied the deciding word (" + supplied[0] + ")")

    if re.search(r"(the student|the learner|the key)", reply or "", re.I):
        bad.append("talked about the student instead of to them")
    if GIVES_AWAY.search(reply or ""):
        bad.append("handed the answer over")
    return bad


def parse_verdict(text):
    """Pull the verdict word off the reply. Returns (verdict or None, message)."""
    t = (text or "").strip()
    m = re.match(r"^\W*verdict\s*[:\-]\s*(right|close|wrong|unclear)\b[^\n]*\n*", t, re.I)
    if m:
        return m.group(1).lower(), t[m.end():].strip()
    m = re.search(r"\bverdict\s*[:\-]\s*(right|close|wrong|unclear)\b", t, re.I)
    if m:
        return m.group(1).lower(), (t[:m.start()] + t[m.end():]).strip()
    return None, t


# --------------------------------------------------------------------------------------------------
#  The fallback, used when the model leaks twice or cannot be reached at all
# --------------------------------------------------------------------------------------------------
def canned(q, hints, verdict=None):
    """A nudge written here, from the question's own clue positions. Safe by construction.

    Used when the model leaks twice or cannot be reached. The verdict, if the model managed to give one,
    still shapes the opening line: one word cannot give anything away.
    """
    spots = [_where(q["story"], c) for c in q.get("clues", [])]
    spot = spots[min(hints, len(spots) - 1)] if spots else "the line that says what must be reported"
    head = {"right": "That is it. ",
            "close": "You are in the right neighbourhood, and what you describe solves a real problem. ",
            "wrong": "",
            "unclear": ""}.get(verdict, "")
    if verdict == "right":
        return (head + "Now earn it properly, so that it was not luck: go to %s and tell me which words in it "
                "settle the matter, and which sentence tells you what must come out at the end." % spot)
    if hints <= 0:
        return (head + "Read the story again and stop at %s. Say that one sentence aloud in your own words, as "
                "if to a friend, then ask whether what you described would hand back exactly the thing it asks "
                "for." % spot)
    if hints == 1:
        return (head + "Go to %s. What does it demand that your method would not give you? Write that down in "
                "one line before you look anywhere else." % spot)
    if hints == 2:
        return (head + "Put your answer beside %s and find the exact point where the two disagree. One of them "
                "is about a different quantity than the other." % spot)
    return (head + "Strip it to a scene: a list of things, and someone who must report one thing at the end. "
            "Looking at %s, what is that one thing, and must it come from a single unbroken piece of the list "
            "or may it be gathered from scattered pieces?" % spot)


# --------------------------------------------------------------------------------------------------
#  The call
# --------------------------------------------------------------------------------------------------
def _ask_one(cfg, model, user, timeout, system=None):
    """One model, one request. Returns (text, error)."""
    payload = {"model": model, "temperature": 0.4, "max_tokens": 600,
               "messages": [{"role": "system", "content": system or JUDGE_PROMPT},
                            {"role": "user", "content": user}]}
    payload.update(llm_config.options_for(model))
    for attempt in range(2):
        try:
            out = call(cfg, "/chat/completions", payload, timeout=timeout)
            text = (out["choices"][0]["message"].get("content") or "").strip()
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
            if not text:                       # a reasoning model that never got to its answer
                return "", "returned nothing (%s)" % out["choices"][0].get("finish_reason")
            return text, None
        except urllib.error.HTTPError as e:
            opts = llm_config.options_for(model)
            if e.code == 400 and opts and any(k in payload for k in opts):
                for k in opts:
                    payload.pop(k, None)       # this model rejects the thinking-off option: retry plain
                continue
            return "", "HTTP %d" % e.code
        except Exception as e:
            return "", type(e).__name__
    return "", "refused the request"


# A model that just failed is skipped for a few minutes, so one dead provider does not add its whole
# timeout to every later call. Cleared when the hub restarts.
_COOLDOWN = {}
COOLDOWN_SECS = 600
TOTAL_SECS = 75        # the endpoint always answers within about this
PER_MODEL_SECS = 50    # one model's share of it

def _chain():
    now = time.time()
    chain = llm_config.model_chain()
    live = [m for m in chain if _COOLDOWN.get(m, 0) < now]
    return live or chain          # everything is cooling down: try them all anyway


def _ask(cfg, case, warn=None, deadline=None):
    """Ask the chosen model, then the fallbacks, within an OVERALL deadline.

    Returns (text, error, model_used, tried). The deadline matters more than any single model: a page that
    hangs for three minutes is worse than one that admits it could not reach the coach. Each model gets
    whatever is left of the budget, capped at PER_MODEL_SECS.
    """
    user = build_judge_message(case)
    if warn:
        user += ("\n\nYour previous reply was rejected because it " + warn +
                 ". Write a new reply that points only at a place in the story, supplies no adjective or "
                 "quantity of its own, quotes nothing from the story, and never names or describes the approach.")
    tried = []
    for model in _chain():
        left = (deadline - time.time()) if deadline else PER_MODEL_SECS
        if left < 8:                       # not enough of the budget left to be worth starting
            tried.append("out of time")
            break
        text, err = _ask_one(cfg, model, user, min(PER_MODEL_SECS, left))
        if not err:
            _COOLDOWN.pop(model, None)
            return text, None, model, tried
        if err != "HTTP 429":              # rate limiting is transient; a timeout is often just a slow moment
            _COOLDOWN[model] = time.time() + (60 if err == "TimeoutError" else COOLDOWN_SECS)
        tried.append("%s (%s)" % (model.split("/")[-1], err))
    return "", "no model answered in time: " + ", ".join(tried), None, tried


def judge(q, answer, hints=0, prior_verdict=None, message=None):
    """Judge one typed answer and return a dict for the page."""
    if not llm_config.is_configured():
        return {"ok": False, "error": "no API key in .env, so the coach is off - mark yourself on the reveal.",
                "verdict": prior_verdict, "reply": canned(q, hints), "source": "offline"}
    cfg = llm_config.load()
    key = key_for(q)
    case = {"story": shown_story(q), "key": key, "answer": answer, "hints_given": hints,
            "prior_verdict": prior_verdict, "message": message, "history": history_for(q)}
    student = " ".join(x for x in (answer, message) if x)

    t0 = time.time()
    deadline = t0 + TOTAL_SECS
    text, err, used, tried = _ask(cfg, case, deadline=deadline)
    if err:
        return {"ok": False, "error": err, "verdict": prior_verdict, "reply": canned(q, hints, prior_verdict),
                "source": "offline", "secs": round(time.time() - t0, 1), "tried": tried}

    verdict, msg = parse_verdict(text)
    bad = leak_check(msg, key, student)
    if bad:
        # One more go, but only if the budget allows. Asking again doubles the wait, and a model that
        # leaked once usually leaks again, so the tool's own nudge is the better trade once time is short.
        if deadline - time.time() > 20:
            text2, err2, used2, tried2 = _ask(cfg, case, warn=bad[0], deadline=deadline)
            tried += tried2
            if not err2 and text2:
                v2, m2 = parse_verdict(text2)
                if not leak_check(m2, key, student):
                    verdict, msg, used, bad = (v2 or verdict), m2, used2, []
                else:
                    msg = canned(q, hints, verdict)
            else:
                msg = canned(q, hints, verdict)
        else:
            msg = canned(q, hints, verdict)
    if verdict not in VERDICTS:
        verdict = prior_verdict or "unclear"
    return {"ok": True, "verdict": verdict, "reply": msg or canned(q, hints, verdict),
            "source": "model" if not bad else "fallback", "secs": round(time.time() - t0, 1),
            "model": used, "leaks": bad, "tried": tried}


def teach(q, answer):
    """The full explanation, for a student who is still stuck after several hints. Nothing is hidden, so no leak check."""
    if not llm_config.is_configured():
        return {"ok": False, "error": "no API key in .env, so the coach is off - use the reveal instead."}
    cfg = llm_config.load()
    case = {"story": shown_story(q), "key": key_for(q), "answer": answer, "history": history_for(q)}
    user = build_teach_message(case)
    deadline = time.time() + TOTAL_SECS
    tried = []
    for model in _chain():
        left = deadline - time.time()
        if left < 8:
            break
        text, err = _ask_one(cfg, model, user, min(PER_MODEL_SECS, left), system=TEACH_PROMPT)
        if not err:
            return {"ok": True, "reply": text, "model": model, "source": "model"}
        tried.append("%s (%s)" % (model.split("/")[-1], err))
    return {"ok": False, "error": "no model answered in time: " + ", ".join(tried)}


# --------------------------------------------------------------------------------------------------
#  The coach's memory of THIS student: what they have missed before, read from their saved progress.
#  It is used for tone and for vocabulary only. It never names a pattern, so it cannot leak the answer.
# --------------------------------------------------------------------------------------------------
PROGRESS = os.path.join(os.path.dirname(HERE), "data", "progress.json")


def history_for(q):
    """A short plain-text summary of the student's history, or '' if there is none yet."""
    try:
        kv = json.load(open(PROGRESS, encoding="utf-8"))
        st = kv.get("mock-oa-v2")
        st = json.loads(st) if isinstance(st, str) else (st or {})
    except Exception:
        return ""
    hist, words, seen = st.get("hist") or [], st.get("words") or {}, st.get("seen") or {}
    lines = []
    if hist:
        n = sum(h.get("n", 0) for h in hist)
        pts = sum(h.get("pts", 0) for h in hist)
        lines.append("%d earlier sittings, %d scenarios, scoring %d%% overall." % (len(hist), n, round(100 * pts / n) if n else 0))
    story = q["story"].lower()
    met = [w for w in words if w.lower() in story]
    if met:
        lines.append("Words in THIS story that they have missed before: " + ", ".join(met[:8]) + ".")
    if seen.get(q["id"]):
        lines.append("They have seen this exact scenario before (%d time(s))." % seen[q["id"]])
    return " ".join(lines)
