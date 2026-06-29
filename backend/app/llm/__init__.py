from app.config import settings
from app.llm.base import LLMProvider, LLMResponse
from app.llm.openai_provider import OpenAIProvider


def get_llm() -> LLMProvider:
    if settings.llm_provider in ("openai", "azure_openai"):
        return OpenAIProvider()
    return OpenAIProvider()


__all__ = ["LLMProvider", "LLMResponse", "get_llm"]
