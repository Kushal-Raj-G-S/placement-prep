"""Shared helpers for the aptitude question generators (apt_gen_a / apt_gen_b)."""
import random
from fractions import Fraction

_rng = random.Random(7)


def fmt(x, unit="", dec=2):
    """Plain number text: ints stay ints, otherwise trimmed decimals."""
    if isinstance(x, Fraction):
        x = float(x)
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            x = int(round(x))
        else:
            x = round(x, dec)
            x = ("%.*f" % (dec, x)).rstrip("0").rstrip(".")
    return f"{x}{unit}"


def mk(t, s, tgt, q, right, wrongs, sc):
    """Build one bank entry. `right`/`wrongs` are already display strings; options get a seeded shuffle."""
    right = str(right)
    seen = {right}
    ws = []
    for w in wrongs:
        w = str(w)
        if w not in seen:
            seen.add(w)
            ws.append(w)
    if len(ws) < 3:
        try:  # numeric answer: top up with near-misses
            rv = float(right)
            for d in (10, -10, 2, -2, 1, -1, 5, -5, 20):
                c = fmt(rv + d if abs(rv) < 30 else rv * (1 + d / 100))
                if c not in seen and len(ws) < 3:
                    seen.add(c)
                    ws.append(c)
        except ValueError:
            pass
    if len(ws) < 3:
        raise ValueError(f"need 3 distinct wrongs for {q[:50]!r}: got {ws}")
    ws = ws[:3]
    opts = [right] + ws
    _rng.shuffle(opts)
    return {"t": t, "s": s, "tgt": tgt, "q": q, "o": opts, "a": opts.index(right), "sc": sc}


def near(v, steps, unit="", dec=2):
    """Plausible nearby wrong values around a number."""
    out = []
    for d in steps:
        out.append(fmt(v + d, unit, dec))
    return out
