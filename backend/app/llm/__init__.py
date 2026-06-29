from app.config import settings
from app.llm.azure_openai_provider import AzureOpenAIProvider
from app.llm.base import LLMProvider, LLMResponse
from app.llm.local_provider import LocalProvider
from app.llm.openai_provider import OpenAIProvider

_PROVIDERS: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "azure_openai": AzureOpenAIProvider,
    "local": LocalProvider,
}


def get_llm() -> LLMProvider:
    name = settings.llm_provider.lower()
    factory = _PROVIDERS.get(name)
    if factory is None:
        supported = ", ".join(sorted(_PROVIDERS))
        raise ValueError(f"Unsupported LLM provider {settings.llm_provider!r}; expected one of: {supported}")
    return factory()


__all__ = ["LLMProvider", "LLMResponse", "get_llm"]
