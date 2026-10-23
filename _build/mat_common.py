"""Authoring helpers for the SQL Lab study guide. Topic files build lists of dicts with these."""


def H(t): return {"k": "h", "t": t}
def P(t): return {"k": "p", "t": t}
def UL(*items): return {"k": "ul", "t": list(items)}
def OL(*items): return {"k": "ol", "t": list(items)}
def NOTE(t): return {"k": "note", "t": t}
def TRAP(t): return {"k": "trap", "t": t}
def ASK(t): return {"k": "ask", "t": t}
def PG(t): return {"k": "pg", "t": t}
def MY(t): return {"k": "my", "t": t}
def DIF(t): return {"k": "dif", "t": t}


def TBL(head, *rows):
    return {"k": "table", "head": list(head), "rows": [list(r) for r in rows]}


def SQL(code, cap=None, run=False):
    """Generic SQL. run=True adds a Run button that executes it on a copy of the sample DB (SQLite)."""
    return {"k": "code", "lang": "sql", "code": code.strip("\n"), "cap": cap, "run": run}


def PGSQL(code, cap=None):
    return {"k": "code", "lang": "pg", "code": code.strip("\n"), "cap": cap, "run": False}


def MYSQL(code, cap=None):
    return {"k": "code", "lang": "my", "code": code.strip("\n"), "cap": cap, "run": False}


def TXT(code, cap=None):
    return {"k": "code", "lang": "txt", "code": code.strip("\n"), "cap": cap, "run": False}


def Q(q, opts, ans, why):
    """One test question. opts is a list of 4 strings, ans the index of the right one."""
    return {"q": q, "o": list(opts), "a": ans, "w": why}


def topic(id, group, title, intro, blocks, test, star=False, kw=""):
    return {"id": id, "group": group, "title": title, "intro": intro, "blocks": blocks,
            "test": test, "star": star, "kw": kw}
