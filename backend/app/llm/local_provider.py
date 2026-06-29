from app.config import settings
from app.llm.base import LLMProvider, LLMResponse
from app.llm.http_chat import build_messages, format_prompt, post_chat_completion


class LocalProvider(LLMProvider):
    """OpenAI-compatible local servers (Ollama, vLLM, etc.)."""

    def __init__(self) -> None:
        self._base = (settings.llm_api_base or "http://localhost:11434/v1").rstrip("/")
        self._model = settings.llm_model
        self._api_key = settings.llm_api_key

    @property
    def available(self) -> bool:
        return bool(self._model)

    def complete(self, prompt: str, system: str = "") -> LLMResponse:
        if not self._model:
            raise RuntimeError("LLM_MODEL must be set for local provider")

        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        messages = build_messages(prompt, system)
        return post_chat_completion(
            url=f"{self._base}/chat/completions",
            headers=headers,
            body={"model": self._model, "messages": messages, "temperature": 0.2},
            provider=settings.llm_provider,
            model=self._model,
            prompt=format_prompt(prompt, system),
        )
