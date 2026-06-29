import httpx

from app.config import settings
from app.llm.base import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self._api_key = settings.llm_api_key
        self._model = settings.llm_model

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def complete(self, prompt: str, system: str = "") -> LLMResponse:
        if not self._api_key:
            raise RuntimeError("LLM API key not configured")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"model": self._model, "messages": messages, "temperature": 0.2},
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]

        return LLMResponse(
            content=content,
            provider=settings.llm_provider,
            model=self._model,
            prompt=prompt if not system else f"[system]\n{system}\n\n[user]\n{prompt}",
        )
