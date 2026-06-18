"""
LLM router — sends messages to the right model based on available credentials.

Priority (auto mode):
  1. Claude  — if key starts with sk-ant-
  2. OpenAI  — if key starts with sk-
  3. Ollama  — default, no key needed, runs locally

Pass model_name to override the default model for any provider.
"""

OLLAMA_MODEL = "llama3.2"
CLAUDE_MODEL = "claude-sonnet-4-6"
OPENAI_MODEL = "gpt-4o-mini"


def chat(messages: list[dict], system_prompt: str,
         api_key: str = "", model_choice: str = "auto",
         model_name: str = "") -> str:
    """
    Send a conversation to an LLM and return the assistant reply as a string.

    messages       — list of {"role": "user"/"assistant", "content": "..."}
    system_prompt  — full system prompt string (built by prompt_builder)
    api_key        — Claude or OpenAI key (leave empty for Ollama)
    model_choice   — "auto" | "claude" | "openai" | "ollama"
    model_name     — specific model id, overrides the provider default when set
    """
    provider = _resolve_provider(api_key, model_choice)

    if provider == "claude":
        return _claude(messages, system_prompt, api_key, model_name or CLAUDE_MODEL)
    elif provider == "openai":
        return _openai(messages, system_prompt, api_key, model_name or OPENAI_MODEL)
    else:
        return _ollama(messages, system_prompt, model_name or OLLAMA_MODEL)


def _resolve_provider(api_key: str, model_choice: str) -> str:
    if model_choice in ("claude", "openai", "ollama"):
        return model_choice
    if api_key.startswith("sk-ant-"):
        return "claude"
    if api_key.startswith("sk-"):
        return "openai"
    return "ollama"


def _claude(messages: list[dict], system_prompt: str, api_key: str, model: str) -> str:
    if not api_key:
        return "[Error] No Claude API key set. Paste your key in Settings → Claude API key."
    try:
        import anthropic
    except ImportError:
        return "[Error] anthropic package not installed — run: pip install anthropic"

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


def _openai(messages: list[dict], system_prompt: str, api_key: str, model: str) -> str:
    if not api_key:
        return "[Error] No OpenAI API key set. Paste your key in Settings → OpenAI API key."
    try:
        from openai import OpenAI
    except ImportError:
        return "[Error] openai package not installed — run: pip install openai"

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def _ollama(messages: list[dict], system_prompt: str, model: str) -> str:
    try:
        import ollama
    except ImportError:
        return "[Error] ollama package not installed — run: pip install ollama"

    response = ollama.chat(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + messages,
    )
    return response["message"]["content"]
