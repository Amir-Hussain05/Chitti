import logging
from skills.base import BaseSkill
from llm.groq_client import GroqClient

logger = logging.getLogger(__name__)

class AssignmentHelperSkill(BaseSkill):

    @property
    def name(self) -> str:
        return "assignment_helper"

    @property
    def triggers(self) -> list[str]:
        return ["assignment", "homework", "explain", "solve",
                "question", "topic", "study", "notes",
                "quiz", "test", "exam", "samjhao", "batao",
                "help me with", "what is", "how does",
                "define", "difference between"]

    def execute(self, text: str) -> str:
        try:
            llm = GroqClient()
            messages = [
                {
                    "role": "system",
                    "content": """You are CHITTI, a smart study companion by Nexora for Amir Baloch.
When helping with assignments or studies:
- Give clear, structured answers
- Use simple language
- Give examples where needed
- Use bullet points for lists
- If it's a question, answer it directly first then explain
- If user asks for notes, give well-organized notes
- If user asks for quiz, give 5 MCQ questions on the topic
- Always respond in the same language the user uses"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            response = llm.chat(messages)
            logger.info("Assignment help given for: %s", text[:50])
            return response

        except Exception as e:
            logger.error("Assignment helper error: %s", e)
            return "Sorry Amir, I could not process that. Please try again."