from abc import ABC, abstractmethod

class BaseMemory(ABC):

    @abstractmethod
    def add(self, role: str, content: str) -> None:
        pass

    @abstractmethod
    def get_history(self) -> list[dict]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass