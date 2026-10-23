# -*- coding: utf-8 -*-
"""
Reads the local .env file (no third-party packages) and exposes the LLM settings.

The API key lives ONLY in .env on this machine. It is read by Python on the server side and sent
straight to the API; it is never written into any HTML page, log line or data file, so the browser
never sees it. Nothing here ever prints the key.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)   # the materials folder (this file lives in _build/)

# Chosen by benchmark (llm_bench.py). Used when NVIDIA_MODEL in .env is empty.
# gpt-oss-20b is the one that actually answers (2026-10-22): glm-5.3-flash and deepseek-v4.1-flash
# were both timing out on every request. Put your own choice in .env as NVIDIA_MODEL to override.
DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
# Extra request options each model needs. Reasoning models burn their whole token budget "thinking" unless told not to.
MODEL_OPTIONS = {
    "nvidia/nemotron-3-ultra-550b-a55b": {"chat_template_kwargs": {"enable_thinking": False}},
    "z-ai/glm-5.3-flash": {"reasoning_effort": "low"},
    "nvidia/nemotron-3.5-lightning-30b-a3b": {"chat_template_kwargs": {"enable_thinking": False}},
    "openai/gpt-oss-20b": {"reasoning_effort": "low"},
}
# Tried in order when the chosen model is unreachable or times out. Providers go down and get
# overloaded; the coach should degrade to a slower or weaker model rather than to nothing.
FALLBACK_MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b",   # picked 2026-10-22: 3-5s, follows the prompt, does not copy examples
    "openai/gpt-oss-20b",
]
ENV_PATH = os.path.join(ROOT, ".env")


def _parse(text):
    out = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        out[k.strip()] = v
    return out


def load():
    """Return {key, base_url, model}. An environment variable wins over the file."""
    vals = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, encoding="utf-8") as f:
            vals = _parse(f.read())

    def pick(name, default=""):
        return os.environ.get(name) or vals.get(name) or default

    return {
        "key": pick("NVIDIA_API_KEY"),
        "base_url": pick("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").rstrip("/"),
        "model": pick("NVIDIA_MODEL", DEFAULT_MODEL),
    }


def is_configured():
    c = load()
    return bool(c["key"]) and bool(c["model"])


def options_for(model):
    return dict(MODEL_OPTIONS.get(model, {}))


def model_chain():
    """The chosen model first, then the fallbacks, with no repeats."""
    out, seen = [], set()
    for m in [load()["model"]] + FALLBACK_MODELS:
        if m and m not in seen:
            seen.add(m); out.append(m)
    return out
