"""
gui/main_window.py

Main application window for CHITTI.

Responsibilities:
- Create the main application layout
- Manage reusable UI components
- Handle navigation events
- Connect UI with AIService

No AI logic should exist here beyond calling the service.
"""

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
)

from gui.widgets.sidebar import Sidebar
from gui.widgets.header import Header
from gui.widgets.chat_area import ChatArea
from gui.widgets.input_bar import InputBar

from services.ai_service import AIService


# ==========================================================
# AI Worker Thread
# ==========================================================

class AIWorker(QThread):
    """
    Runs AI requests in a separate thread.
    """

    finished = Signal(str)

    def __init__(self, prompt: str):
        super().__init__()

        self.prompt = prompt
        self.ai = AIService()

    def run(self):
        response = self.ai.ask(self.prompt)
        self.finished.emit(response)


# ==========================================================
# Main Window
# ==========================================================

class MainWindow(QMainWindow):
    """
    Main window for CHITTI.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CHITTI by Nexora")
        self.resize(1400, 850)
        self.setMinimumSize(1100, 700)

        self._build_ui()

    # ======================================================

    def _build_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_requested.connect(
            self.on_navigation
        )

        root_layout.addWidget(self.sidebar)

        # Workspace
        workspace = QWidget()

        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        # Header
        self.header = Header()
        workspace_layout.addWidget(self.header)

        # Chat
        self.chat_area = ChatArea()
        workspace_layout.addWidget(self.chat_area, 1)

        # Input
        self.input_bar = InputBar()
        self.input_bar.message_sent.connect(
            self.on_message_sent
        )

        workspace_layout.addWidget(self.input_bar)

        root_layout.addWidget(workspace, 1)

    # ======================================================

    def on_navigation(self, page: str):

        print(page)

    # ======================================================

    def on_message_sent(self, text: str):
        """
        Called whenever user presses Send.
        """

        if not text.strip():
            return

        # Show user message
        self.chat_area.add_message(
            text,
            "user"
        )

        # Update status
        self.header.set_status("🤖 Thinking...")

        # Disable input while AI is responding
        self.input_bar.setEnabled(False)

        # Start worker thread
        self.worker = AIWorker(text)
        self.worker.finished.connect(self.on_ai_response)
        self.worker.start()

    # ======================================================

    def on_ai_response(self, response: str):
        """
        Called when AI finishes.
        """

        self.chat_area.add_message(
            response,
            "assistant"
        )

        self.header.set_status("🟢 Ready")

        self.input_bar.setEnabled(True)