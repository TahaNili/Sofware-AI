"""
Main entry point of the application
"""

import sys
import logging
import traceback
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from agent.windows.system import WindowsController
from agent.ai.factory import AIFactory
from PySide6.QtCore import qInstallMessageHandler, QtMsgType

# Load environment variables from .env early so factory and clients see them
load_dotenv()


# Configure simple console + file logging
LOG_FILENAME = "sofware_ai_error.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FILENAME, encoding="utf-8")],
)
logger = logging.getLogger(__name__)


def _excepthook(exc_type, exc_value, exc_tb):
    """Global exception hook that logs unhandled exceptions to console and file."""
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    # Print to stdout so setup_and_run.bat captures it in the console
    print("Unhandled exception:\n", tb)
    logger.error("Unhandled exception:\n%s", tb)


sys.excepthook = _excepthook


def main():
    # Create Qt application
        # Create Qt application
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # Install Qt message handler to forward Qt warnings/errors to console
        def qt_message_handler(msg_type: QtMsgType, context, message: str):
            # Map Qt message types to a label
            typ = {
                0: "Debug",
                1: "Info",
                2: "Warning",
                3: "Critical",
                4: "Fatal",
            }.get(int(msg_type), "Log")
            print(f"[Qt {typ}] {message}")

        qInstallMessageHandler(qt_message_handler)

        # Ensure KeyboardInterrupt still exits normally and let sys.excepthook handle others
        def handle_exception(exc_type, exc_value, exc_tb):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_tb)
                return
            # Use the unified excepthook that logs to console and file
            _excepthook(exc_type, exc_value, exc_tb)

        sys.excepthook = handle_exception

        try:
            window = MainWindow(agent_factory=AIFactory)
            window.show()
            # Run the event loop; exceptions in callbacks will go to the excepthook
            exit_code = app.exec()
            sys.exit(exit_code)
        except Exception:
            # Log startup-time exceptions and re-raise so exit code is non-zero
            _excepthook(*sys.exc_info())
            raise