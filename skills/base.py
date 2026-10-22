from abc import ABC, abstractmethod

class BaseSkill(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def triggers(self) -> list[str]:
        pass

    def can_handle(self, text: str) -> bool:
        text_lower = text.lower()
        return any(trigger in text_lower for trigger in self.triggers)

    @abstractmethod
    def execute(self, text: str) -> str:
        pass