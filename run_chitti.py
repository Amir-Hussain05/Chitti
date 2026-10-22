"""
CHITTI Application Entry Point

This file starts the complete desktop application.

Responsibilities:
- Start CHITTI
- Launch GUI

Business logic should NOT exist here.
"""

from gui.app import ChittiApplication


def main():
    app = ChittiApplication()
    app.run()


if __name__ == "__main__":
    main()