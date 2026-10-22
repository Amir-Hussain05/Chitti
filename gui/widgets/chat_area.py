"""
gui/widgets/chat_area.py

Chat workspace for CHITTI.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from gui.chat.chat_container import ChatContainer
from gui.chat.message_widget import MessageWidget


class ChatArea(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.welcome = QLabel(
            "👋 Welcome to CHITTI\n\nHow can I help you today?"
        )

        self.welcome.setObjectName("WelcomeLabel")

        self.chat_container = ChatContainer()

        layout.addWidget(self.welcome)
        layout.addWidget(self.chat_container)

    def add_message(self, message: str, sender: str):

        # Hide welcome screen after first message
        if self.welcome is not None:
            self.welcome.hide()
            self.welcome = None

        is_user = sender == "user"

        message_widget = MessageWidget(
            message,
            is_user,
        )

        self.chat_container.add_message(
            message_widget
        )