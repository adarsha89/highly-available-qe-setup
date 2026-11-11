"""Configurable AI provider for the /api/ai/insights endpoint.

Selection and model are controlled entirely through environment variables so the
underlying AI model can be swapped without code changes:

  AI_PROVIDER     "ollama" | "anthropic" | "openai" | "rule_based" (default: "ollama")
  AI_MODEL        model name for the chosen provider
                  (default: "llama3.1" for ollama, "claude-sonnet-5" for anthropic,
                  "gpt-4o-mini" for openai)
  OLLAMA_HOST        Ollama server URL (default: http://localhost:11434)
  ANTHROPIC_API_KEY  required when AI_PROVIDER=anthropic
  OPENAI_API_KEY     required when AI_PROVIDER=openai

If a provider is requested but its API key is missing, or it fails to initialize or
respond (e.g. no local Ollama server running), the app falls back to the built-in
rule-based provider so insights are always available.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...


class RuleBasedProvider(AIProvider):
    name = "rule_based"

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("RuleBasedProvider builds insights directly from structured data")


class OllamaProvider(AIProvider):
    def __init__(self, model: str, host: Optional[str] = None):
        import ollama

        self.client = ollama.Client(host=host) if host else ollama.Client()
        self.model = model
        self.name = f"ollama:{model}"

    def generate(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]


class AnthropicProvider(AIProvider):
    def __init__(self, model: str, api_key: str):
        import anthropic

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.name = f"anthropic:{model}"

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text")


class OpenAIProvider(AIProvider):
    def __init__(self, model: str, api_key: str):
        import openai

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.name = f"openai:{model}"

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


def get_provider() -> AIProvider:
    provider_name = os.getenv("AI_PROVIDER", "ollama").lower()

    if provider_name == "ollama":
        try:
            return OllamaProvider(model=os.getenv("AI_MODEL", "llama3.1"), host=os.getenv("OLLAMA_HOST"))
        except Exception:
            pass

    if provider_name == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                return AnthropicProvider(model=os.getenv("AI_MODEL", "claude-sonnet-5"), api_key=api_key)
            except Exception:
                pass

    if provider_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                return OpenAIProvider(model=os.getenv("AI_MODEL", "gpt-4o-mini"), api_key=api_key)
            except Exception:
                pass

    return RuleBasedProvider()
