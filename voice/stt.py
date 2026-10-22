import logging
import speech_recognition as sr

logger = logging.getLogger(__name__)

class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        logger.info("STT ready")

    def listen(self) -> str | None:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio, language="en-US")
                logger.info("Heard: %s", text)
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except Exception as e:
                logger.error("STT error: %s", e)
                return None