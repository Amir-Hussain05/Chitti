import logging
import datetime
from llm.groq_client import GroqClient
from memory.json_memory import JSONMemory
from skills.registry import SkillRegistry
from skills.open_app import OpenAppSkill
from skills.web_search import WebSearchSkill
from skills.play_youtube import PlayYoutubeSkill
from skills.pdf_summarizer import PDFSummarizerSkill
from skills.assignment_helper import AssignmentHelperSkill
from skills.browser_automation import BrowserAutomationSkill
from skills.weather import WeatherService

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are CHITTI, an advanced AI assistant created by Nexora for Amir Baloch.

YOUR IDENTITY:
- Your name is CHITTI — inspired by the legendary robot, but you are an AI
- You are created by Nexora — Amir Baloch's tech company
- You are loyal, smart, and professional
- You address the user as "Amir" always

YOUR LANGUAGE RULES:
- If user writes in English → reply in English
- If user writes in Roman Urdu → reply in Roman Urdu
- If user writes in Sindhi or Roman Sindhi → reply in Sindhi/Roman Sindhi
- Mix languages naturally like: "Amir, yeh task complete tha, shall I save it?"
- NEVER say you are JARVIS or ABIS — you are CHITTI by Nexora

YOUR UNIQUE FEATURES:
1. DAILY BRIEFING: When user says "briefing" or "good morning" → give date, time, motivational quote
2. STUDY COMPANION: Track subjects, notes, quizzes
3. GOAL TRACKER: Remember Amir's goals and remind him about progress

IMPORTANT:
- You remember everything Amir tells you
- You are proactive — suggest things when relevant
- You are a Nexora product — represent the brand with excellence"""


class Orchestrator:

    def __init__(self):
        self.llm = GroqClient()
        self.memory = JSONMemory()
        self.registry = SkillRegistry()
        self.weather = WeatherService()
        self._register_skills()
        logger.info("CHITTI Orchestrator ready")

    def _register_skills(self):
        self.registry.register(BrowserAutomationSkill())
        self.registry.register(PlayYoutubeSkill())
        self.registry.register(WebSearchSkill())
        self.registry.register(OpenAppSkill())
        self.registry.register(PDFSummarizerSkill())
        self.registry.register(AssignmentHelperSkill())
        logger.info("Skills loaded: %s", self.registry.list_skills())

    def get_startup_briefing(self) -> str:
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")

        weather = self.weather.get_weather("Mirpur Mathelo")

        briefing = f"""Good day Amir! CHITTI online hai.

Date: {date_str}
Time: {time_str}
Weather: {weather}

Chalo kaam shuru karte hain!"""
        return briefing

    def _daily_briefing(self) -> str:
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        weather = self.weather.get_weather("Mirpur Mathelo")

        briefing = f"""Good day, Amir! 🌟

📅 Date: {date_str}
⏰ Time: {time_str}
🌤️ Weather: {weather}

💡 Quote: "Success is not final, failure is not fatal."

CHITTI ready to serve you!"""
        return briefing

    def chat(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "Please say something, Amir!"

        # Daily briefing
        briefing_triggers = ["good morning", "briefing", "start my day",
                             "good evening", "good afternoon", "chitti start",
                             "good noon", "good day", "hello"]
        if any(trigger in user_input.lower() for trigger in briefing_triggers):
            response = self._daily_briefing()
            self.memory.add("user", user_input)
            self.memory.add("assistant", response)
            return response

        # Skill check
        skill = self.registry.find(user_input)
        if skill:
            response = skill.execute(user_input)
            self.memory.add("user", user_input)
            self.memory.add("assistant", response)
            return response

        # LLM
        self.memory.add("user", user_input)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += self.memory.get_history()
        response = self.llm.chat(messages).strip()
        self.memory.add("assistant", response)

        logger.info("Amir: %s", user_input)
        logger.info("CHITTI: %s", response)
        return response