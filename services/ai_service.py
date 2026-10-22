"""
services/ai_service.py

Handles all communication with the Groq API.
"""

import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()


class AIService:
    """
    Handles communication with the Groq LLM.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env"
            )

        self.model = os.getenv(
            "JARVIS_LLM_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.client = Groq(api_key=api_key)

    # ==============================================
    # Main public method used throughout CHITTI
    # ==============================================

    def ask(self, prompt: str) -> str:
        """
        Public method used by the GUI.
        """
        return self.generate_response(prompt)

    # ==============================================
    # Internal Groq request
    # ==============================================

    def generate_response(self, prompt: str) -> str:
        """
        Send a prompt to Groq and return the response.
        """

        try:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
            )

            response = completion.choices[0].message.content

            if response:
                return response.strip()

            return "I couldn't generate a response."

        except Exception as e:

            return f"⚠️ AI Error: {str(e)}"