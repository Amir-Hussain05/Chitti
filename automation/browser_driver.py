import logging
from playwright.sync_api import sync_playwright, Browser, Page

logger = logging.getLogger(__name__)

class BrowserDriver:

    def __init__(self, headless: bool = False):
        self.headless = headless
        self._playwright = None
        self._browser: Browser = None
        self._page: Page = None

    def start(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            args=["--start-maximized"]
        )
        self._page = self._browser.new_page()
        logger.info("Browser started")

    def goto(self, url: str):
        self._page.goto(url, wait_until="domcontentloaded")
        logger.info("Navigated to: %s", url)

    def search_google(self, query: str):
        import urllib.parse
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        self.goto(url)
        logger.info("Google search: %s", query)

    def click(self, selector: str):
        self._page.click(selector)
        logger.info("Clicked: %s", selector)

    def type_text(self, selector: str, text: str):
        self._page.fill(selector, text)
        logger.info("Typed in %s: %s", selector, text)

    def get_title(self) -> str:
        return self._page.title()

    def get_url(self) -> str:
        return self._page.url

    def screenshot(self, path: str = "screenshot.png"):
        self._page.screenshot(path=path)
        logger.info("Screenshot saved: %s", path)

    def close(self):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        logger.info("Browser closed")