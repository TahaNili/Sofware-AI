"""
Main UI of the application using PySide6
"""

import sys
from typing import Optional
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QTextEdit, QPushButton, QLabel, QProgressBar)
from PySide6.QtCore import Qt, Slot, QThread, Signal
from PySide6.QtGui import QFont, QIcon
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
        self.setWindowTitle("دستیار هوشمند ویندوز")
        self.setMinimumSize(800, 600)
        
        # Set Persian font
        font = QFont("Vazir", 10)
        QApplication.setFont(font)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 10px;
                font-size: 12pt;
            }
        """)
        layout.addWidget(self.chat_area)
        
        # User input
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText("دستور خود را اینجا وارد کنید...")
        layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("ارسال")
        self.send_button.clicked.connect(self.on_send)
        layout.addWidget(self.send_button)
        
        # Status bar
        self.status_bar = QProgressBar()
        self.status_bar.setTextVisible(False)
        layout.addWidget(self.status_bar)
        
        # Set up worker thread
        self.worker = None
        
        # Welcome message
        self.add_message("سیستم", "سلام! من دستیار هوشمند شما هستم. چطور می‌تونم کمکتون کنم؟")

    def add_message(self, sender: str, message: str):
        """اضافه کردن پیام به ناحیه چت"""
        self.chat_area.append(f"<b>{sender}:</b> {message}<br>")

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