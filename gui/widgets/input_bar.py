"""
gui/widgets/input_bar.py

Reusable message input widget for CHITTI.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class InputBar(QWidget):
    """
    Bottom input widget.
    """

    message_sent = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("InputBar")

        self._build_ui()

    def _build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        # -----------------------
        # Message Box
        # -----------------------

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Message CHITTI..."
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        # -----------------------
        # Voice Button
        # -----------------------

        self.voice_button = QPushButton("🎤")

        self.voice_button.setFixedSize(42, 42)

        # -----------------------
        # Send Button
        # -----------------------

        self.send_button = QPushButton("Send")

        self.send_button.setFixedHeight(42)

        self.send_button.clicked.connect(
            self.send_message
        )

        layout.addWidget(self.voice_button)

        layout.addWidget(self.input)

        layout.addWidget(self.send_button)

    def send_message(self):

        text = self.input.text().strip()

        if not text:
            return

        self.message_sent.emit(text)

        self.input.clear()