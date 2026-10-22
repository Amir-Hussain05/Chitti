import json
import logging
from memory.base import BaseMemory
from configs.settings import settings

logger = logging.getLogger(__name__)

class JSONMemory(BaseMemory):

    def __init__(self):
        self.path = settings.memory_full_path
        self.max_turns = settings.memory_max_turns
        self.history = self._load()
        logger.info("JSONMemory loaded — %d messages", len(self.history))

    def _load(self) -> list[dict]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self.history, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]
        self._save()

    def get_history(self) -> list[dict]:
        return self.history.copy()

    def clear(self) -> None:
        self.history = []
        self._save()
        logger.info("Memory cleared")

    def get_today_date(self) -> str:
        import datetime
        return datetime.date.today().strftime("%Y-%m-%d")