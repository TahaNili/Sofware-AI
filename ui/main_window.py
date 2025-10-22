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
from PySide6.QtGui import QFont, QFontDatabase, QIcon
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

    def run(self) -> None:
        try:
            if self.command is None:
                self.progress.emit("There are no commands to execute.")
                return
            result = self.agent.process_command(self.command)
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
        self.agent = self.agent_factory()
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
        
        # AI Provider selection
        provider_label = QLabel("مدل هوش مصنوعی:")
        self.provider_combo = QComboBox()
        self.provider_combo.addItem("Google Gemini", "gemini")
        self.provider_combo.addItem("OpenAI", "openai")
        self.provider_combo.currentIndexChanged.connect(self.on_provider_changed)
        
        # Model selection
        model_label = QLabel("نوع مدل:")
        self.model_combo = QComboBox()
        self.update_model_list()
        
        # CLI Button (right-aligned)
        self.cli_button = QPushButton("اجرا در خط فرمان")
        self.cli_button.setObjectName("cliButton")
        self.cli_button.clicked.connect(self.run_cli)
        
        # Add widgets with proper spacing
        layout.addWidget(provider_label)
        layout.addWidget(self.provider_combo)
        layout.addWidget(model_label)
        layout.addWidget(self.model_combo)
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

        # Add welcome message
        welcome_text = """سلام! 👋\nمن دستیار هوشمند شما هستم و می‌توانم در موارد مختلف به شما کمک کنم.\n\nمی‌توانید از من بپرسید:\n• جستجو و مقایسه قیمت محصولات\n• تحلیل و بررسی محصولات\n• پیشنهاد محصولات مشابه\n• راهنمایی برای خرید\n• مدیریت سیستم و برنامه‌ها\n\nهر سؤالی دارید، با خیال راحت بپرسید! 😊"""
        self.show_message("سیستم", welcome_text)
        
        # Scroll area for chat
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Chat container
        chat_container = QWidget()
        self.chat_layout = QVBoxLayout(chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(20)
        scroll_area.setWidget(chat_container)
        main_layout.addWidget(scroll_area)
        
        # Bottom panel for input
        bottom_panel = QWidget()
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(0, 10, 0, 10)
        
        # Message input
        self.input_field = QTextEdit()
        self.input_field.setObjectName("messageInput")
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText("پیام خود را اینجا بنویسید...")
        
        # Send button
        self.send_button = QPushButton("ارسال")
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.on_send)
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add input and button to bottom panel
        bottom_layout.addWidget(self.input_field)
        bottom_layout.addWidget(self.send_button)
        main_layout.addWidget(bottom_panel)
        
        # Progress bar for loading state
        self.status_bar = QProgressBar()
        self.status_bar.setTextVisible(False)
        self.status_bar.setMaximumHeight(2)
        main_layout.addWidget(self.status_bar)
        
        # Worker thread setup
        self.worker = None
        
        # Add welcome message
        welcome_text = """سلام! 👋\nمن دستیار هوشمند شما هستم و می‌توانم در موارد مختلف به شما کمک کنم.\n\nمی‌توانید از من بپرسید:\n• جستجو و مقایسه قیمت محصولات\n• تحلیل و بررسی محصولات\n• پیشنهاد محصولات مشابه\n• راهنمایی برای خرید\n• مدیریت سیستم و برنامه‌ها\n\nهر سؤالی دارید، با خیال راحت بپرسید! 😊"""
        self.show_message("سیستم", welcome_text)

    def update_model_list(self):
        """Update available models based on selected provider"""
        provider = self.provider_combo.currentData()
        self.model_combo.clear()
        
        if provider == "gemini":
            self.model_combo.addItems(["gemini-pro", "gemini-1.5-pro"])
        else:
            self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4"])
            
    def on_provider_changed(self):
        """Handle AI provider change"""
        self.update_model_list()
        provider = self.provider_combo.currentData()
        self.agent = self.agent_factory(
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
        
        # Create and start async task
        async def process_message():
            try:
                # Process request
                response = await self.agent.process_request(user_input)
                
                # Handle different response types
                if isinstance(response, dict):
                    if response.get('error'):
                        self.show_error(str(response['error']))
                    elif response.get('response'):
                        self.show_message("سیستم", str(response['response']))
                    elif response.get('analysis'):
                        self.show_message("تحلیل", str(response['analysis']))
                    elif response.get('recommendations'):
                        recommendations = response.get('recommendations', [])
                        if isinstance(recommendations, list):
                            self.show_message("پیشنهادات", "\n".join(map(str, recommendations)))
                        else:
                            self.show_message("پیشنهادات", str(recommendations))
                elif response is not None:
                    self.show_message("سیستم", str(response))
            except Exception as e:
                self.show_error(f"خطا در پردازش درخواست: {str(e)}")
            finally:
                self.set_input_enabled(True)
        
        # Run async task
        asyncio.ensure_future(process_message())

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