import logging
from groq import Groq
from llm.base import BaseLLMClient
from configs.settings import settings

logger = logging.getLogger(__name__)

class GroqClient(BaseLLMClient):

    def __init__(self):
        self.client = Groq(api_key=settings.anthropic_api_key)
        self.model = settings.llm_model
        logger.info("GroqClient ready — model: %s", self.model)

    def chat(self, messages: list[dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Groq API error: %s", e)
            return "Sorry, I could not get a response. Please try again."