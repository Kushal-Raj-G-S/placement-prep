# -*- coding: utf-8 -*-
"""
Is the NVIDIA API wired up?   python llm_check.py

  step 1  is a key present in .env?
  step 2  can that key reach the API and list models?   (saves the ids to data/llm_models.json)
  step 3  does the chosen NVIDIA_MODEL answer a tiny question, and how fast?

It prints status only. It never prints the key.
"""
import json, os, sys, time, urllib.request, urllib.error
import llm_config

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def call(cfg, path, payload=None, timeout=60):
    url = cfg["base_url"] + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if payload is not None else "GET")
    req.add_header("Authorization", "Bearer " + cfg["key"])
    req.add_header("Accept", "application/json")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def explain(e):
    if isinstance(e, urllib.error.HTTPError):
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        hint = {401: "the key was rejected - re-copy it from build.nvidia.com",
                403: "the key is valid but not allowed to use that - check the model or your account",
                404: "that model id or path does not exist - run this script and pick an id from the list",
                429: "rate limited - wait a minute and retry"}.get(e.code, "unexpected response")
        return "HTTP %d: %s. %s" % (e.code, hint, body)
    return "%s: %s" % (type(e).__name__, e)


def main():
    cfg = llm_config.load()
    print("1) key in .env ...", end=" ")
    if not cfg["key"]:
        print("MISSING\n   Open .env, paste your key after NVIDIA_API_KEY=, save, and run this again.")
        return 1
    print("present (%d characters)" % len(cfg["key"]))

    print("2) reaching %s ..." % cfg["base_url"], end=" ")
    try:
        t = time.time()
        listing = call(cfg, "/models")
        ids = sorted(m.get("id", "") for m in listing.get("data", []) if m.get("id"))
        print("OK, %d models, %.1fs" % (len(ids), time.time() - t))
    except Exception as e:
        print("FAILED\n   " + explain(e))
        return 1
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "llm_models.json"), "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=0)
    print("   saved the full list to data/llm_models.json")
    likely = [i for i in ids if any(w in i.lower() for w in
              ("llama", "nemotron", "qwen", "deepseek", "mistral", "gemma", "phi"))]
    print("   chat-style models that look usable (first 40 of %d):" % len(likely))
    for i in likely[:40]:
        print("     " + i)

    print("3) chosen model ...", end=" ")
    if not cfg["model"]:
        print("not set yet\n   Pick an id from the list above and put it after NVIDIA_MODEL= in .env.")
        return 0
    try:
        t = time.time()
        out = call(cfg, "/chat/completions", {
            "model": cfg["model"], "temperature": 0, "max_tokens": 400,
            "messages": [{"role": "user", "content": "Reply with exactly the word READY and nothing else."}],
            **llm_config.options_for(cfg["model"])}, timeout=120)
        reply = out["choices"][0]["message"]["content"].strip()
        print("OK in %.1fs, it said: %r" % (time.time() - t, reply[:60]))
    except Exception as e:
        print("FAILED\n   " + explain(e))
        return 1
    print("\nAll three steps passed. The environment is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
