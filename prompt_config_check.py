import importlib
import os
import sys


def import_prompt(provider, model):
    old_provider = os.environ.get("LLM_PROVIDER")
    old_model = os.environ.get("DEFAULT_MODEL")
    os.environ["LLM_PROVIDER"] = provider
    os.environ["DEFAULT_MODEL"] = model
    sys.modules.pop("prompt", None)

    try:
        return importlib.import_module("prompt")
    finally:
        sys.modules.pop("prompt", None)
        if old_provider is None:
            os.environ.pop("LLM_PROVIDER", None)
        else:
            os.environ["LLM_PROVIDER"] = old_provider
        if old_model is None:
            os.environ.pop("DEFAULT_MODEL", None)
        else:
            os.environ["DEFAULT_MODEL"] = old_model


def check_gemini_provider_does_not_keep_ollama_model():
    prompt = import_prompt("gemini", "gemma3:4b")
    assert prompt.PROVIDER == "gemini"
    assert prompt.DEFAULT_MODEL == "gemini-2.5-flash"


if __name__ == "__main__":
    check_gemini_provider_does_not_keep_ollama_model()
