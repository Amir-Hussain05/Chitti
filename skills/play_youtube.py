import subprocess
import logging
import pywhatkit
from skills.base import BaseSkill

logger = logging.getLogger(__name__)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class PlayYoutubeSkill(BaseSkill):

    @property
    def name(self) -> str:
        return "play_youtube"

    @property
    def triggers(self) -> list[str]:
        return ["play", "youtube", "video", "song", "music", "chalao", "bajao"]

    def execute(self, text: str) -> str:
        query = text.lower()
        for trigger in self.triggers:
            query = query.replace(trigger, "")
        query = query.strip()

        if not query:
            return "Amir, kya play karun?"

        try:
            import urllib.parse
            encoded = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={encoded}"
            subprocess.Popen([CHROME_PATH, "--new-window", url])
            logger.info("YouTube opened in Chrome: %s", query)
            return f"Playing '{query}' on YouTube in Chrome!"
        except FileNotFoundError:
            logger.error("Chrome not found at: %s", CHROME_PATH)
            try:
                pywhatkit.playonyt(query)
                return f"Playing '{query}' on YouTube!"
            except Exception as e:
                logger.error("pywhatkit error: %s", e)
                return f"Could not play '{query}'. Please try again."
        except Exception as e:
            logger.error("YouTube error: %s", e)
            return f"Could not play '{query}'. Please try again."