import subprocess
import logging
from skills.base import BaseSkill

logger = logging.getLogger(__name__)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class OpenAppSkill(BaseSkill):

    @property
    def name(self) -> str:
        return "open_app"

    @property
    def triggers(self) -> list[str]:
        return ["open chrome", "open notepad", "open calculator",
                "open vlc", "open word", "open excel",
                "open explorer", "open paint", "open vs code",
                "open vscode", "launch chrome", "launch notepad",
                "start chrome", "chrome kholo", "notepad kholo",
                "calculator kholo"]

    APP_MAP = {
        "chrome": CHROME_PATH,
        "notepad": "notepad",
        "calculator": "calc",
        "vlc": "vlc",
        "word": "winword",
        "excel": "excel",
        "file explorer": "explorer",
        "explorer": "explorer",
        "paint": "mspaint",
        "vs code": "code",
        "vscode": "code",
    }

    def can_handle(self, text: str) -> bool:
        text_lower = text.lower()
        # Sirf tab handle karo jab koi app name ho
        return any(trigger in text_lower for trigger in self.triggers)

    def execute(self, text: str) -> str:
        text_lower = text.lower()

        for app_name, app_cmd in self.APP_MAP.items():
            if app_name in text_lower:
                try:
                    subprocess.Popen(app_cmd, shell=True)
                    logger.info("Opened app: %s", app_name)
                    return f"Opening {app_name} for you!"
                except Exception as e:
                    logger.error("Failed to open %s: %s", app_name, e)
                    return f"Sorry, I could not open {app_name}."

        return "Which app would you like me to open? Try saying 'open chrome' or 'open notepad'."