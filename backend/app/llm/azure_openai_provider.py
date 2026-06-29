from app.config import settings
from app.llm.base import LLMProvider, LLMResponse
from app.llm.http_chat import build_messages, format_prompt, post_chat_completion


class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI uses deployment-scoped URLs and an api-key header."""

    def __init__(self) -> None:
        self._api_key = settings.llm_api_key
        self._deployment = settings.llm_model
        self._endpoint = settings.llm_api_base.rstrip("/")
        self._api_version = settings.llm_api_version

    @property
    def available(self) -> bool:
        return bool(self._api_key and self._endpoint and self._deployment)

    def complete(self, prompt: str, system: str = "") -> LLMResponse:
        if not self.available:
            raise RuntimeError("Azure OpenAI requires LLM_API_KEY, LLM_API_BASE, and LLM_MODEL (deployment)")

        messages = build_messages(prompt, system)
        url = (
            f"{self._endpoint}/openai/deployments/{self._deployment}/chat/completions"
            f"?api-version={self._api_version}"
        )
        return post_chat_completion(
            url=url,
            headers={"api-key": self._api_key, "Content-Type": "application/json"},
            body={"messages": messages, "temperature": 0.2},
            provider=settings.llm_provider,
            model=self._deployment,
            prompt=format_prompt(prompt, system),
        )
