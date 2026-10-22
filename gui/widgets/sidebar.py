"""
gui/widgets/sidebar.py

Reusable Sidebar Widget for CHITTI Desktop AI Assistant.

Responsibilities:
- Display application logo
- Display navigation buttons
- Emit navigation events

This widget contains NO business logic.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


class Sidebar(QWidget):
    """
    Reusable sidebar component.
    """

    # Emitted when a navigation button is clicked.
    navigation_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(240)

        self.buttons = {}

        self._build_ui()

    def _build_ui(self):
        """Create sidebar layout."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(12)

        # Logo
        self.logo = QLabel("🤖 CHITTI")
        self.logo.setObjectName("SidebarLogo")
        self.logo.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.logo)
        layout.addSpacing(25)

        # Navigation Buttons
        self._add_button(layout, "💬", "Chat")
        self._add_button(layout, "🧠", "Memory")
        self._add_button(layout, "🧩", "Plugins")
        self._add_button(layout, "⚙", "Settings")

        layout.addStretch()

    def _add_button(self, layout, icon, text):
        """
        Create and add a navigation button.
        """

        button = QPushButton(f"{icon}  {text}")

        button.setObjectName("SidebarButton")
        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(
            lambda _, page=text: self.navigation_requested.emit(page)
        )

        layout.addWidget(button)

        self.buttons[text] = button