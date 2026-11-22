"""One small helper for calling a language model, whichever provider you use.

    import llm
    llm.setup("gemini")          # or "claude", "openai", or "replay" (no key needed)
    print(llm.ask("hi", system="You are Northstar's admissions assistant."))

"replay" mode needs no account: it returns answers recorded for the course notebooks,
so every notebook runs from start to finish. Switch to a live model when you're ready.
"""
import getpass
import json
import os
import re

from recorded import RECORDED

# Model names change often. If one stops working, check the provider's model list and change it here.
MODELS = {
    "gemini": "gemini-3.8-flash",     # on Gemini's free tier
    "claude": "claude-haiku-5-5",
    "openai": "gpt-6-luna",
}
KEY_NAMES = {"gemini": "GEMINI_API_KEY", "claude": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}

provider = None
_client = None
usage = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
_replay_count = {}


def _get_key(name):
    """Read an API key from Colab secrets, then the environment, then ask for it."""
    try:
        from google.colab import userdata
        key = userdata.get(name)
        if key:
            return key
    except Exception:
        pass
    return os.environ.get(name) or getpass.getpass(f"Paste your {name} (it stays hidden): ")


def setup(name):
    """Choose a provider: "gemini", "claude", "openai" or "replay"."""
    global provider, _client
    provider = name
    _replay_count.clear()
    if name == "replay":
        print("Replay mode: answers are recorded examples, not a live model. No key needed.")
        return
    key = _get_key(KEY_NAMES[name])
    if name == "gemini":
        from google import genai
        _client = genai.Client(api_key=key)
    elif name == "claude":
        import anthropic
        _client = anthropic.Anthropic(api_key=key)
    elif name == "openai":
        import openai
        _client = openai.OpenAI(api_key=key)
    else:
        raise ValueError('Choose "gemini", "claude", "openai" or "replay".')
    print(f"Using {name} ({MODELS[name]}).")


def ask(prompt, system="", temperature=0.0, label=None):
    """Send one message, with optional rules (system), and return the model's reply as text.

    label names the step in a course notebook, so replay mode can find its recorded answer.
    """
    if provider is None:
        raise RuntimeError('Run llm.setup(...) first, e.g. llm.setup("replay").')
    usage["calls"] += 1
    if provider == "replay":
        answers = RECORDED.get(label)
        if answers is None:
            return "(No recorded answer for this one. Switch to a live model to try your own prompts.)"
        if isinstance(answers, str):
            return answers
        i = _replay_count.get(label, 0)
        _replay_count[label] = i + 1
        return answers[i % len(answers)]

    if provider == "gemini":
        from google.genai import types
        r = _client.models.generate_content(
            model=MODELS["gemini"], contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system or None, temperature=temperature))
        meta = getattr(r, "usage_metadata", None)
        if meta:
            usage["input_tokens"] += meta.prompt_token_count or 0
            usage["output_tokens"] += meta.candidates_token_count or 0
        return r.text

    if provider == "claude":
        # Claude's current API has no temperature setting, so it isn't sent.
        r = _client.messages.create(model=MODELS["claude"], max_tokens=1024, system=system,
                                    messages=[{"role": "user", "content": prompt}])
        usage["input_tokens"] += r.usage.input_tokens
        usage["output_tokens"] += r.usage.output_tokens
        return "".join(b.text for b in r.content if b.type == "text")

    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    try:
        r = _client.chat.completions.create(model=MODELS["openai"], messages=messages, temperature=temperature)
    except Exception as e:                       # some models only accept their default temperature
        if "temperature" not in str(e):
            raise
        r = _client.chat.completions.create(model=MODELS["openai"], messages=messages)
    if r.usage:
        usage["input_tokens"] += r.usage.prompt_tokens
        usage["output_tokens"] += r.usage.completion_tokens
    return r.choices[0].message.content


def ask_json(prompt, system="", temperature=0.0, label=None):
    """Like ask, but the reply must be JSON. Returns a dictionary."""
    text = ask(prompt, system=system, temperature=temperature, label=label)
    match = re.search(r"\{.*\}", text, re.S)     # models sometimes wrap JSON in ``` or a sentence
    if not match:
        raise ValueError(f"The model didn't reply with JSON:\n{text}")
    return json.loads(match.group(0))
