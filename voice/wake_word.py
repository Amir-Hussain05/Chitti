import logging
import threading
import speech_recognition as sr

logger = logging.getLogger(__name__)

class WakeWordDetector:

    def __init__(self, wake_word: str = "chitti"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.5
        self._triggered = False
        logger.info("Wake word detector ready — listening for: %s", wake_word)

    def listen_for_wake_word(self) -> bool:
        print("\n🎤 Say 'Chitti' OR press ENTER to activate...")

        self._triggered = False
        keyboard_thread = threading.Thread(target=self._wait_for_enter)
        keyboard_thread.daemon = True
        keyboard_thread.start()

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            while not self._triggered:
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=3,
                        phrase_time_limit=4
                    )
                    text = self.recognizer.recognize_google(
                        audio,
                        language="en-US"
                    ).lower()
                    logger.info("Heard: %s", text)

                    wake_triggers = ["chitti", "hey chitti",
                                     "hello chitti", "chitty",
                                     "cheety", "cheeti", "chiti"]
                    if any(trigger in text for trigger in wake_triggers):
                        self._triggered = True
                        return True

                except sr.WaitTimeoutError:
                    if self._triggered:
                        return True
                    continue
                except sr.UnknownValueError:
                    if self._triggered:
                        return True
                    continue
                except Exception as e:
                    logger.error("Wake word error: %s", e)
                    if self._triggered:
                        return True
                    continue

        return self._triggered

    def _wait_for_enter(self):
        input()
        self._triggered = True

    def close(self):
        pass