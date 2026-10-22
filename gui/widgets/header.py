"""
gui/widgets/header.py

Reusable application header for CHITTI.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)


class Header(QWidget):
    """
    Reusable top header.
    """

    def __init__(self):
        super().__init__()

        self.setObjectName("Header")

        self._build_ui()

    def _build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # -----------------------------
        # Title
        # -----------------------------

        self.title = QLabel("🤖 CHITTI")

        self.title.setObjectName("HeaderTitle")

        # -----------------------------
        # Spacer
        # -----------------------------

        layout.addWidget(self.title)

        layout.addStretch()

        # -----------------------------
        # Status
        # -----------------------------

        self.status = QLabel("🟢 Ready")

        self.status.setObjectName("StatusLabel")

        layout.addWidget(self.status)

    def set_status(self, text):
        """
        Update AI status.
        """

        self.status.setText(text)