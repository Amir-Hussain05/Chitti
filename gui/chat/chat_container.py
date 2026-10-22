"""
gui/chat/chat_container.py

Scrollable container that holds all chat messages.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
)


class ChatContainer(QWidget):

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.content = QWidget()

        # Center conversation column
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(180, 25, 180, 25)
        self.layout.setSpacing(12)

        # Push conversation to top
        self.layout.addStretch()

        self.scroll.setWidget(self.content)

        root.addWidget(self.scroll)

    def add_message(self, message_widget):

        self.layout.insertWidget(
            self.layout.count() - 1,
            message_widget,
        )

        scrollbar = self.scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())