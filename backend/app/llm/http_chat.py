import httpx

from app.llm.base import LLMResponse


def post_chat_completion(
    *,
    url: str,
    headers: dict[str, str],
    body: dict,
    provider: str,
    model: str,
    prompt: str,
) -> LLMResponse:
    with httpx.Client(timeout=60.0) as client:
        resp = client.post(url, headers=headers, json=body)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

    return LLMResponse(content=content, provider=provider, model=model, prompt=prompt)


def build_messages(prompt: str, system: str = "") -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return messages


def format_prompt(prompt: str, system: str = "") -> str:
    if not system:
        return prompt
    return f"[system]\n{system}\n\n[user]\n{prompt}"
