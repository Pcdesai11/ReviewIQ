from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    prompt: str


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str, system: str = "") -> LLMResponse:
        pass

    @property
    def available(self) -> bool:
        return True
