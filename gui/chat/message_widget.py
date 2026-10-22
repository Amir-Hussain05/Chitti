"""
gui/chat/message_widget.py

Wraps a chat bubble and aligns it left/right.
"""

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from gui.chat.chat_bubble import ChatBubble


class MessageWidget(QWidget):
    """
    One complete message row.
    """

    def __init__(self, text, is_user=False):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)

        bubble = ChatBubble(text, is_user)

        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()