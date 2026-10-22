"""
Background worker for AI requests.

Runs Groq requests in another thread so the GUI never freezes.
"""

from PySide6.QtCore import QObject, Signal, Slot

from services.ai_service import AIService


class AIWorker(QObject):

    finished = Signal(str)

    error = Signal(str)

    def __init__(self):
        super().__init__()

        self.ai = AIService()

    @Slot(str)
    def process(self, prompt):

        try:

            response = self.ai.ask(prompt)

            self.finished.emit(response)

        except Exception as e:

            self.error.emit(str(e))