"""
gui/chat/chat_bubble.py

Professional chat bubble widget.
"""

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)
from PySide6.QtCore import Qt


class ChatBubble(QFrame):

    def __init__(self, text, is_user=False):
        super().__init__()

        self.is_user = is_user

        self.setMaximumWidth(700)

        if is_user:
            self.setObjectName("UserBubble")
        else:
            self.setObjectName("AssistantBubble")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18,
            12,
            18,
            12,
        )

        layout.setSpacing(0)

        self.label = QLabel(text)

        self.label.setWordWrap(True)

        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # IMPORTANT
        # Remove the black rectangle behind text
        self.label.setStyleSheet("""
        QLabel{
            background: transparent;
            border: none;
            color: white;
        }
        """)

        layout.addWidget(self.label)