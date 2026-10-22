import logging
import subprocess
import urllib.parse
from skills.base import BaseSkill

logger = logging.getLogger(__name__)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class BrowserAutomationSkill(BaseSkill):

    @property
    def name(self) -> str:
        return "browser_automation"

    @property
    def triggers(self) -> list[str]:
        return ["open website", "go to", "browse", "website kholo",
                "open link", "navigate to", "visit", "open youtube",
                "open google", "open facebook", "open instagram",
                "open github", "open netflix"]

    def execute(self, text: str) -> str:
        url = self._extract_url(text)
        if not url:
            return "Amir, kaunsi website kholun? Example: 'open website youtube.com'"

        if not url.startswith("http"):
            url = "https://" + url

        try:
            subprocess.Popen([
                CHROME_PATH,
                "--new-window",
                "--no-first-run",
                "--no-default-browser-check",
                url
            ])
            logger.info("Website opened in Chrome: %s", url)
            return f"Opening {url} in Chrome!"
        except FileNotFoundError:
            import webbrowser
            webbrowser.open(url)
            return f"Opening {url}!"
        except Exception as e:
            logger.error("Browser error: %s", e)
            return f"Website nahi khul saki: {e}"

    def _extract_url(self, text: str) -> str | None:
        text_lower = text.lower()

        # Known websites
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "github": "https://www.github.com",
            "netflix": "https://www.netflix.com",
            "whatsapp": "https://web.whatsapp.com",
            "gmail": "https://mail.google.com",
            "twitter": "https://www.twitter.com",
            "linkedin": "https://www.linkedin.com",
        }

        for site, url in sites.items():
            if site in text_lower:
                return url

        # URL directly text mein hai
        words = text_lower.split()
        skip = ["open", "website", "go", "to", "browse",
                "kholo", "link", "navigate", "visit", "open website"]
        for word in words:
            if word not in skip and "." in word:
                return word

        return None