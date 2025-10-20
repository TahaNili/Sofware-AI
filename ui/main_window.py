"""
Modern chat-based main window implementation using PySide6
"""

import sys
import os
from typing import Optional
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QTextEdit, QPushButton, QLabel, QProgressBar,
                              QScrollArea, QFrame, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QFontDatabase
from ui import styles  # Import our custom styles
from PySide6.QtCore import Qt, Slot, QThread, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QFontDatabase
from . import styles  # Import our custom styles
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
                self.progress.emit("هیچ دستوری برای اجرا وجود ندارد")
                return
            result = self.agent.process_command(self.command)
            self.finished.emit(result)
        except Exception as e:
            self.progress.emit(f"خطا: {str(e)}")
            self.progress.emit(f"خطا: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.setWindowTitle("Sofware AI - دستیار هوشمند")
        self.setMinimumSize(900, 700)
        
        # Message history
        self.messages = []
        
        # Initialize font
        font = QFont()
        font.setPointSize(11)
        
        # Try to load Vazir font if available
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "Vazir.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id >= 0:
                font.setFamily("Vazir")
        else:
            # Fall back to system font with good Persian support
            for family in ["Tahoma", "Arial", "Segoe UI"]:
                font.setFamily(family)
                if font.exactMatch():
                    break
        QApplication.setFont(font)
        
        # Apply modern styles
        self.setStyleSheet(styles.STYLE)
        
        # Central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
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
        welcome_text = """سلام! 👋
من دستیار هوشمند شما هستم و می‌توانم در موارد مختلف به شما کمک کنم.

می‌توانید از من بپرسید:
• جستجو و مقایسه قیمت محصولات
• تحلیل و بررسی محصولات
• پیشنهاد محصولات مشابه
• راهنمایی برای خرید
• مدیریت سیستم و برنامه‌ها

هر سؤالی دارید، با خیال راحت بپرسید! 😊"""
        self.show_message("سیستم", welcome_text)
        
    def show_message(self, sender: str, message: str):
        """Add a new message to the chat layout"""
        # Store in history
        self.messages.append({"sender": sender, "message": message})
        
        # Create message container
        msg_container = QWidget()
        msg_container.setObjectName("messageContainer")
        msg_layout = QVBoxLayout(msg_container)
        msg_layout.setContentsMargins(10, 10, 10, 10)
        
        # Sender label
        sender_label = QLabel(sender)
        sender_label.setObjectName("messageSender")
        msg_layout.addWidget(sender_label)
        
        # Message content
        msg_content = QLabel(message)
        msg_content.setObjectName("messageContent")
        msg_content.setWordWrap(True)
        msg_layout.addWidget(msg_content)
        
        # Add message to chat layout
        self.chat_layout.addWidget(msg_container)
        
        # Ensure new message is visible
        msg_container.show()
        QApplication.processEvents()
        
    def show_error(self, message: str):
        """Show error message in chat"""
        self.show_message("خطا", message)
        
    def show_system_message(self, message: str):
        """Show system message in chat"""
        self.show_message("سیستم", message)
        
    def on_send_sync(self):
        """Handle send button click (synchronous fallback)"""
        # Get user input
        user_input = self.input_field.toPlainText().strip()
        if not user_input:
            return
            
        # Clear input field
        self.input_field.clear()
        
        # Show user message
        self.show_message("شما", user_input)
        
        # Disable input while processing
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.status_bar.setMaximum(0)  # Show indeterminate progress
        
        try:
            # Process request through agent
            response = self.agent.process_request(user_input)
            self.show_message("سیستم", response)
            
        except Exception as e:
            self.show_error(f"خطا در پردازش درخواست: {str(e)}")
            
        finally:
            # Re-enable input
            self.input_field.setEnabled(True)
            self.send_button.setEnabled(True)
            self.status_bar.setMaximum(100)  # Hide progress bar

    def add_message(self, sender: str, message: str):
        """اضافه کردن پیام به ناحیه چت"""
        return True  # For future expansion

    @Slot()
    def on_send(self):
        """پردازش دستور کاربر"""
        command = self.input_field.toPlainText().strip()
        if not command:
            return
            
        self.add_message("شما", command)
        self.input_field.clear()
        # Start processing in a separate thread
        self.status_bar.setMaximum(0)
        self.worker = WorkerThread(self.agent)
        self.worker.command = command
        self.worker.finished.connect(self.on_result)
        self.worker.progress.connect(self.on_progress)
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