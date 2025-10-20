"""Modern and clean Qt styling for the application"""

STYLE = """/* Main Window */
QMainWindow {
    background-color: #ffffff;
}

/* Scrollbars */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    width: 12px;
    margin: 0px;
    background-color: #f5f5f5;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #dadce0;
    min-height: 30px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #bdc1c6;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Message Containers */
QWidget#messageContainer {
    background-color: #f8f9fa;
    border-radius: 12px;
    border: 1px solid #dadce0;
}

QWidget#messageContainer:hover {
    border-color: #bdc1c6;
}

QLabel#messageSender {
    font-weight: bold;
    color: #202124;
    font-size: 13px;
    padding: 2px;
}

QLabel#messageContent {
    color: #3c4043;
    font-size: 14px;
    line-height: 1.5;
    padding: 4px;
}

/* Input Area */
QTextEdit#messageInput {
    background-color: #f8f9fa;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 14px;
    color: #3c4043;
    selection-background-color: #e8f0fe;
}

QTextEdit#messageInput:hover {
    border-color: #bdc1c6;
}

QTextEdit#messageInput:focus {
    border-color: #1a73e8;
    background-color: #ffffff;
}

/* Send Button */
QPushButton#sendButton {
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 24px;
    font-size: 14px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton#sendButton:hover {
    background-color: #1557b0;
}

QPushButton#sendButton:pressed {
    background-color: #174ea6;
}

QPushButton#sendButton:disabled {
    background-color: #dadce0;
}

/* Progress Bar */
QProgressBar {
    border: none;
    background-color: transparent;
}

QProgressBar::chunk {
    background-color: #1a73e8;
}

/* Chat Area */
QTextEdit#chatArea {
    background-color: #ffffff;
    border: none;
    padding: 15px;
    font-size: 14pt;
    selection-background-color: #e8f0fe;
}

/* Message Input */
QTextEdit#messageInput {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 20px;
    padding: 10px 15px;
    margin: 10px;
    font-size: 12pt;
}

/* Send Button */
QPushButton#sendButton {
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
    font-size: 12pt;
    min-width: 100px;
}

QPushButton#sendButton:hover {
    background-color: #1557b0;
}

QPushButton#sendButton:pressed {
    background-color: #174ea6;
}

/* System Message */
.system-message {
    background-color: #f8f9fa;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
}

/* User Message */
.user-message {
    background-color: #e8f0fe;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
}

/* Loading Indicator */
QProgressBar {
    border: none;
    background-color: transparent;
    height: 2px;
}

QProgressBar::chunk {
    background-color: #1a73e8;
}
"""