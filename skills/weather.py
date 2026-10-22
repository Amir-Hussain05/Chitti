import requests
import logging

logger = logging.getLogger(__name__)

class WeatherService:

    def get_weather(self, city: str = "Mirpur Mathelo") -> str:
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                weather = response.text.strip()
                logger.info("Weather fetched: %s", weather)
                return weather
            else:
                return "Weather unavailable right now."
        except Exception as e:
            logger.error("Weather error: %s", e)
            return "Could not fetch weather."