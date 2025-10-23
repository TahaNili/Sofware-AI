"""
Modern chat-based main window implementation using PySide6.
Follows Material Design principles and supports RTL layouts for Persian text.
"""

import sys
import os
from typing import Optional, Dict, List
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QPushButton, QLabel, QProgressBar,
    QScrollArea, QFrame, QHBoxLayout, QSizePolicy, 
    QComboBox, QStackedWidget
)
from PySide6.QtCore import Qt, Slot, QThread, Signal, QSize, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QTextCursor
from . import styles
import asyncio
class WorkerThread(QThread):
    """Class for managing async operations"""
    finished = Signal(dict)
    progress = Signal(str)

    def __init__(self, agent) -> None:
        super().__init__()
        self.agent = agent
        self.command: Optional[str] = None
        self._result = None

    def run(self) -> None:
        try:
            if self.command is None:
                self.progress.emit("There are no commands to execute.")
                return
            # agent.process_request is async; run it in this thread's context
            try:
                result = asyncio.run(self.agent.process_request(self.command))
            except Exception as e:
                result = {"type": "error", "error": str(e)}
            self.finished.emit(result)
        except Exception as e:
            self.progress.emit(f"error: {str(e)}")
            self.progress.emit(f"error: {str(e)}")

class MainWindow(QMainWindow):
    """Main application window implementing a modern chat interface with RTL support."""
    
    def __init__(self, agent_factory):
        super().__init__()
        
        # Initialize core components
        self.agent_factory = agent_factory
        self.agent = self.agent_factory.create_client()
        self.messages: List[Dict] = []
        self.worker = None
        self.setup_window()
        self.setup_font()
        self.init_ui()
        self.show_welcome_message()
        
    def setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("Sofware AI - دستیار هوشمند")
        self.setMinimumWidth(800)  # More responsive minimum size
        self.setMinimumHeight(600)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)  # RTL support
        
    def setup_font(self):
        """Initialize and configure fonts with proper fallbacks"""
        font = QFont()
        font.setPointSize(11)
        
        # Try loading Vazir font
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Vazir.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id >= 0:
                font.setFamily("Vazir")
        else:
            # Fallback fonts with good Persian support
            for family in ["Tahoma", "Arial", "Segoe UI"]:
                font.setFamily(family)
                if font.exactMatch():
                    break
                    
        QApplication.setFont(font)
        self.setStyleSheet(styles.STYLE)
        
    def init_ui(self):
        """Initialize and setup the user interface"""
        # Main layout setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add major UI sections
        main_layout.addWidget(self.create_header_panel())
        main_layout.addWidget(self.create_chat_area())
        main_layout.addWidget(self.create_input_panel())
        main_layout.addWidget(self.create_status_bar())
        
    def create_header_panel(self) -> QWidget:
        """Create the top panel with AI model selection"""
        panel = QWidget()
        panel.setObjectName("headerPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # AI Provider selection with status
        provider_label = QLabel("سرویس هوش مصنوعی:")
        self.provider_combo = QComboBox()
        
        # Get available providers from factory
        providers = self.agent_factory.get_available_providers()
        for display_name, provider_id in providers:
            self.provider_combo.addItem(display_name, provider_id)
            
        self.provider_combo.currentIndexChanged.connect(self.on_provider_changed)
        
        # Model selection with tooltip
        model_label = QLabel("نوع مدل:")
        self.model_combo = QComboBox()
        self.model_combo.setToolTip("مدل‌های در دسترس بر اساس کلید API انتخاب می‌شوند")
        self.update_model_list()
        
        # API Status indicator
        self.api_status = QLabel()
        self.api_status.setObjectName("apiStatus")
        self.update_api_status()
        
        # CLI Button (right-aligned)
        self.cli_button = QPushButton("اجرا در خط فرمان")
        self.cli_button.setObjectName("cliButton")
        self.cli_button.clicked.connect(self.run_cli)
        
        # Add widgets with proper spacing
        layout.addWidget(provider_label)
        layout.addWidget(self.provider_combo)
        layout.addWidget(model_label)
        layout.addWidget(self.model_combo)
        layout.addWidget(self.api_status)
        layout.addStretch()
        layout.addWidget(self.cli_button)
        
        return panel
        
    def create_chat_area(self) -> QWidget:
        """Create the scrollable chat area"""
        # Scroll area setup
        scroll = QScrollArea()
        scroll.setObjectName("chatScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Chat container
        container = QWidget()
        self.chat_layout = QVBoxLayout(container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(0, 8, 0, 8)
        
        scroll.setWidget(container)
        return scroll
        
    def create_input_panel(self) -> QWidget:
        """Create the bottom input panel"""
        panel = QWidget()
        panel.setObjectName("inputPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Message input
        self.input_field = QTextEdit()
        self.input_field.setObjectName("messageInput")
        self.input_field.setPlaceholderText("پیام خود را اینجا بنویسید...")
        self.input_field.setAcceptRichText(False)
        cursor = self.input_field.textCursor()
        # move to end using the QTextCursor enum constant
        cursor.movePosition(QTextCursor.End)
        block_fmt = cursor.blockFormat()
        block_fmt.setAlignment(Qt.AlignmentFlag.AlignRight)
        cursor.mergeBlockFormat(block_fmt)
        self.input_field.setTextCursor(cursor)
        
        # Send button
        self.send_button = QPushButton("ارسال")
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.on_send)
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Setup layout
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        
        return panel
        
    def create_status_bar(self) -> QProgressBar:
        """Create the status/progress bar"""
        self.status_bar = QProgressBar()
        self.status_bar.setTextVisible(False)
        self.status_bar.setMaximumHeight(2)
        return self.status_bar

        

    def update_api_status(self):
        """Update the API status indicator based on available keys"""
        provider = self.provider_combo.currentData()
        
        # Set initial loading state
        self.api_status.setText("در حال بررسی...")
        self.api_status.setProperty("status", "loading")
        self.api_status.style().unpolish(self.api_status)
        self.api_status.style().polish(self.api_status)
        
        # Check API key status
        has_key = False
        if provider == "gemini":
            has_key = bool(os.getenv('GOOGLE_API_KEY'))
        elif provider == "openai":
            has_key = bool(os.getenv('OPENAI_API_KEY'))
        else:
            has_key = True  # Mock client always available
            
        # Update status after a small delay to show loading state
        QTimer.singleShot(500, lambda: self._update_api_status_ui(has_key))
        
    def _update_api_status_ui(self, has_key: bool):
        """Update API status UI elements"""
        if has_key:
            self.api_status.setText("✓ متصل")
            self.api_status.setProperty("status", "available")
        else:
            self.api_status.setText("⚠️ کلید API یافت نشد")
            self.api_status.setProperty("status", "unavailable")
        
        # Force style refresh
        self.api_status.style().unpolish(self.api_status)
        self.api_status.style().polish(self.api_status)
        
    def update_model_list(self):
        """Update available models based on selected provider"""
        provider = self.provider_combo.currentData()
        self.model_combo.clear()
        
        # Get models from factory
        models = self.agent_factory.get_models(provider)
        self.model_combo.addItems(models)
        
        # Update API status
        self.update_api_status()
            
    def on_provider_changed(self):
        """Handle AI provider change"""
        self.update_model_list()
        provider = self.provider_combo.currentData()
        self.agent = self.agent_factory.create_client(
            provider=provider,
            model=self.model_combo.currentText()
        )
        
    def run_cli(self):
        """Launch CLI mode in a separate process"""
        import subprocess
        subprocess.Popen([sys.executable, "-m", "agent.cli"])
        
    def show_message(self, sender: str, message: str):
        """Add a new message to the chat area with proper styling"""
        # Store in history
        self.messages.append({"sender": sender, "message": message})
        
        # Create message container with proper styling
        msg_container = QWidget()
        msg_container.setObjectName("messageContainer")
        msg_container.setProperty("sender", sender.lower())  # For CSS styling
        
        msg_layout = QVBoxLayout(msg_container)
        msg_layout.setContentsMargins(12, 12, 12, 12)
        msg_layout.setSpacing(4)
        
        # Sender label with proper RTL support
        sender_label = QLabel(sender)
        sender_label.setObjectName("messageSender")
        sender_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        msg_layout.addWidget(sender_label)
        
        # Message content with proper text wrapping
        msg_content = QLabel(message)
        msg_content.setObjectName("messageContent")
        msg_content.setWordWrap(True)
        msg_content.setTextFormat(Qt.TextFormat.PlainText)
        msg_content.setAlignment(Qt.AlignmentFlag.AlignRight)
        msg_layout.addWidget(msg_content)
        
        # Add to chat and ensure visibility
        self.chat_layout.addWidget(msg_container)
        self.ensure_message_visible(msg_container)
        
    def ensure_message_visible(self, widget: QWidget):
        """Ensure the newest message is visible"""
        scroll_area = self.findChild(QScrollArea, "chatScroll")
        if scroll_area:
            scroll_bar = scroll_area.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())
        widget.show()
        QApplication.processEvents()
        
    def show_error(self, message: str):
        """Display error message in chat"""
        self.show_message("خطا", message)
        
    def show_system_message(self, message: str):
        """Display system message in chat"""
        self.show_message("سیستم", message)
        
    def show_welcome_message(self):
        """Display initial welcome message"""
        welcome_text = (
            "سلام! 👋\n"
            "من دستیار هوشمند شما هستم و می‌توانم در موارد مختلف به شما کمک کنم.\n\n"
            "می‌توانید از من بپرسید:\n"
            "• جستجو و مقایسه قیمت محصولات\n"
            "• تحلیل و بررسی محصولات\n"
            "• پیشنهاد محصولات مشابه\n"
            "• راهنمایی برای خرید\n"
            "• مدیریت سیستم و برنامه‌ها\n\n"
            "هر سؤالی دارید، با خیال راحت بپرسید! 😊"
        )
        self.show_message("سیستم", welcome_text)
        
    def set_input_enabled(self, enabled: bool):
        """Enable/disable input controls"""
        self.input_field.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        self.status_bar.setMaximum(0 if not enabled else 100)
        
    @Slot()
    def on_send(self):
        """Handle message sending with proper async support"""
        user_input = self.input_field.toPlainText().strip()
        if not user_input:
            return
            
        # Clear input and show user message
        self.input_field.clear()
        self.show_message("شما", user_input)
        
        # Disable input during processing
        self.set_input_enabled(False)
        # Create a worker thread to run the agent call (runs asyncio in thread)
        self.worker = WorkerThread(self.agent)
        self.worker.command = user_input
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.progress.connect(self._on_worker_progress)
        self.worker.start()

    @Slot(dict)
    def on_result(self, result: dict):
        """نمایش نتیجه"""
        self.status_bar.setMaximum(100)
        self.status_bar.setValue(100)
        self.add_message("سیستم", str(result))

    @Slot(str)
    def on_progress(self, message: str):
        """نمایش پیشرفت عملیات"""
        self.add_message("سیستم", message)

    def _on_worker_progress(self, message: str):
        # Show progress messages in the UI
        self.show_system_message(message)

    def _on_worker_finished(self, result: dict):
        # Handle worker result and re-enable inputs
        try:
            if isinstance(result, dict):
                if result.get('error'):
                    self.show_error(str(result['error']))
                elif result.get('response'):
                    self.show_message('سیستم', str(result['response']))
                elif result.get('analysis'):
                    self.show_message('تحلیل', str(result['analysis']))
                elif result.get('recommendations'):
                    recommendations = result.get('recommendations', [])
                    if isinstance(recommendations, list):
                        self.show_message('پیشنهادات', '\n'.join(map(str, recommendations)))
                    else:
                        self.show_message('پیشنهادات', str(recommendations))
                elif result.get('type') == 'product_search' and result.get('search_params'):
                    # For product search, delegate to executor via planner or executor
                    search_params = result.get('search_params', {})
                    self.show_message('سیستم', str(search_params.get('response', ''))) 
                else:
                    # Fallback: show the whole result
                    self.show_message('سیستم', str(result))
            else:
                self.show_message('سیستم', str(result))
        finally:
            self.set_input_enabled(True)