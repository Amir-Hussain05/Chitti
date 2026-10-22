"""
gui/app.py

Creates and starts the CHITTI GUI application.

Responsibilities:
- Initialize QApplication
- Set application information
- Load global stylesheet
- Create MainWindow
- Start the event loop

No AI logic should exist here.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


class ChittiApplication:
    """Bootstrap class for the CHITTI desktop application."""

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.app.setApplicationName("CHITTI")
        self.app.setOrganizationName("Nexora")
        self.app.setOrganizationDomain("nexora.ai")

        self._load_stylesheet()

        self.window = MainWindow()

    def _load_stylesheet(self):
        """Load the global QSS theme."""

        qss_file = (
            Path(__file__).parent
            / "styles"
            / "dark_theme.qss"
        )

        if qss_file.exists():
            with open(qss_file, "r", encoding="utf-8") as file:
                self.app.setStyleSheet(file.read())

    def run(self):
        """Show the window and start the event loop."""

        self.window.show()

        sys.exit(self.app.exec())