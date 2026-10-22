import logging
import asyncio
import edge_tts
import pygame
import io
import threading

logger = logging.getLogger(__name__)

class TextToSpeech:

    def __init__(self):
        pygame.mixer.init()
        self.voice = "en-US-AriaNeural"
        self.rate = "+0%"
        logger.info("Edge TTS ready — voice: %s", self.voice)

    def speak(self, text: str) -> None:
        try:
            clean = self._clean_text(text)
            if not clean.strip():
                return
            logger.info("Speaking: %s", clean[:50])
            asyncio.run(self._speak_async(clean))
        except Exception as e:
            logger.error("TTS error: %s", e)

    async def _speak_async(self, text: str) -> None:
        try:
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]

            if audio_data:
                audio_file = io.BytesIO(audio_data)
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
        except Exception as e:
            logger.error("Edge TTS async error: %s", e)

    def _clean_text(self, text: str) -> str:
        replacements = ["*", "#", "📅", "⏰", "💡", "🌟", "📄", "🎯", "✅", "🎤", "🌤️"]
        for r in replacements:
            text = text.replace(r, "")
        return text.strip()