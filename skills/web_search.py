import webbrowser
import logging
from skills.base import BaseSkill

logger = logging.getLogger(__name__)

class WebSearchSkill(BaseSkill):

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def triggers(self) -> list[str]:
        return ["search", "google", "look up", "find", "dhundo", "search karo"]

    def execute(self, text: str) -> str:
        query = text.lower()

        for trigger in self.triggers:
            query = query.replace(trigger, "")

        query = query.strip()

        if not query:
            return "What would you like me to search for?"

        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        logger.info("Searching Google for: %s", query)
        return f"Searching Google for: {query}"