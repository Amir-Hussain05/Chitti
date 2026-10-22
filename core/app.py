import logging
import sys
from configs.settings import settings
from core.logging_setup import setup_logging

logger = logging.getLogger(__name__)

def bootstrap() -> None:
    setup_logging()
    logger.info("Booting %s (env=%s)", settings.app_name, settings.env)
    problems = settings.validate_required()
    if problems:
        for problem in problems:
            logger.error("Config problem: %s", problem)
        sys.exit(1)
    logger.info("Configuration OK.")

def run() -> None:
    bootstrap()
    logger.info("%s online.", settings.app_name)

    from core.orchestrator import Orchestrator
    from voice.tts import TextToSpeech
    from voice.stt import SpeechToText

    orchestrator = Orchestrator()
    tts = TextToSpeech()
    stt = SpeechToText()

    print("\n=============================")
    print("  CHITTI is online!")
    print("  A Nexora AI Product")
    print("  Say 'Chitti' or press ENTER")
    print("  Press Q to quit")
    print("=============================\n")

    # Startup briefing
    startup = orchestrator.get_startup_briefing()
    print(f"CHITTI: {startup}\n")
    tts.speak(startup)

    print("Wake word mode chahiye? (Y/N)")
    wake_choice = input("Choose: ").strip().lower()

    if wake_choice == "y":
        _run_wake_word_mode(orchestrator, tts, stt)
    else:
        _run_manual_mode(orchestrator, tts, stt)


def _run_wake_word_mode(orchestrator, tts, stt):
    from voice.wake_word import WakeWordDetector
    detector = WakeWordDetector()

    tts.speak("Wake word mode active. Say Chitti to activate me.")

    try:
        while True:
            detected = detector.listen_for_wake_word()
            if detected:
                tts.speak("Yes Amir, I am listening.")
                print("CHITTI: Yes Amir! Listening...")

                user_input = stt.listen()
                if not user_input:
                    tts.speak("I did not catch that.")
                    continue

                print(f"You said: {user_input}")

                if user_input.lower() in ("quit", "exit", "goodbye", "band karo"):
                    tts.speak("Allah Hafiz Amir!")
                    print("CHITTI: Allah Hafiz, Amir!")
                    break

                response = orchestrator.chat(user_input)
                first_response = response.split("\nCHITTI:")[0].strip()
                print(f"CHITTI: {first_response}\n")
                tts.speak(first_response)

    except KeyboardInterrupt:
        tts.speak("Allah Hafiz Amir!")
        print("\nCHITTI: Allah Hafiz, Amir!")
    finally:
        detector.close()


def _run_manual_mode(orchestrator, tts, stt):
    try:
        while True:
            print("\n[T] Type  [V] Voice  [Q] Quit")
            choice = input("Choose: ").strip().lower()

            if choice == "q":
                tts.speak("Allah Hafiz Amir!")
                print("CHITTI: Allah Hafiz, Amir!")
                break

            elif choice == "v":
                user_input = stt.listen()
                if not user_input:
                    print("CHITTI: I did not catch that.")
                    tts.speak("I did not catch that.")
                    continue
                print(f"You said: {user_input}")

            else:
                user_input = choice if choice not in ["t", ""] else input("You: ").strip()
                if not user_input:
                    continue

            if user_input.lower() in ("quit", "exit", "bye", "goodbye", "band karo"):
                tts.speak("Allah Hafiz Amir!")
                print("CHITTI: Allah Hafiz, Amir!")
                break

            response = orchestrator.chat(user_input)
            first_response = response.split("\nCHITTI:")[0].strip()
            print(f"CHITTI: {first_response}\n")
            tts.speak(first_response)

    except KeyboardInterrupt:
        tts.speak("Allah Hafiz Amir!")
        print("\nCHITTI: Allah Hafiz, Amir!")


if __name__ == "__main__":
    run()