from abc import ABC, abstractmethod

class BaseLLMClient(ABC):

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass