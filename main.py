"""
Main entry point of the application
"""

import sys
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from agent.windows.system import WindowsController
from agent.ai.factory import AIFactory
import traceback
from PySide6.QtCore import qInstallMessageHandler, QtMsgType

# Load environment variables from .env early so factory and clients see them
load_dotenv()

def main():
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # Install Qt message handler to forward Qt warnings/errors to console
    def qt_message_handler(msg_type: QtMsgType, context, message: str):
        # Map Qt message types to a label
        typ = {
            0: 'Debug',
            1: 'Info',
            2: 'Warning',
            3: 'Critical',
            4: 'Fatal'
        }.get(int(msg_type), 'Log')
        print(f"[Qt {typ}] {message}")

    qInstallMessageHandler(qt_message_handler)

    # Global excepthook to ensure unhandled exceptions are printed to console
    def handle_exception(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            # let KeyboardInterrupt exit normally
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        print("Unhandled exception:", file=sys.stderr)
        traceback.print_exception(exc_type, exc_value, exc_tb)

    sys.excepthook = handle_exception
    window = MainWindow(agent_factory=AIFactory)
    window.show()
    # Run the event loop and ensure exceptions propagate to excepthook
    try:
        rc = app.exec()
    except Exception:
        # Print traceback and re-raise to allow sys.excepthook to run
        traceback.print_exc()
        raise
    sys.exit(rc)

if __name__ == "__main__":
    main()