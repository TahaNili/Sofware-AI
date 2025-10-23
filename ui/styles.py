"""Modern and clean Qt styling for the application following Material Design principles"""

STYLE = """
/* Global Settings */
* {
    font-family: "Vazir", "Tahoma", "Segoe UI", "Arial", sans-serif;
}

QMainWindow {
    background-color: #ffffff;
}

/* Common Components */
QWidget {
    font-size: 14px;
    color: #202124;
}

/* Header Section */
QWidget#headerPanel {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 16px;
    margin: 0;
}

/* API Status Indicator */
QLabel#apiStatus {
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 4px;
    min-width: 80px;
    text-align: center;
}

QLabel#apiStatus[status="available"] {
    background-color: #e6f4ea;
    color: #1e8e3e;
    border: 1px solid #1e8e3e;
}

QLabel#apiStatus[status="unavailable"] {
    background-color: #fce8e6;
    color: #d93025;
    border: 1px solid #d93025;
}

QLabel#apiStatus[status="loading"] {
    background-color: #e8f0fe;
    color: #1a73e8;
    border: 1px solid #1a73e8;
}

QComboBox {
    background-color: #f8f9fa;
    border: 1px solid #dadce0;
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 150px;
}

QComboBox:hover {
    border-color: #1a73e8;
    background-color: #f1f3f4;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: url(resources/down-arrow.png);
    width: 12px;
    height: 12px;
}

QLabel {
    font-weight: 500;
    margin-right: 8px;  /* RTL support */
}

/* Chat Area */
QScrollArea {
    border: none;
    background-color: transparent;
    margin: 0;
    padding: 0;
}

QScrollArea#chatScroll {
    background-color: #f8f9fa;
}

QScrollBar:vertical {
    width: 12px;
    margin: 0;
    background-color: transparent;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #dadce0;
    min-height: 48px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #bdc1c6;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

/* Message Containers */
QWidget#messageContainer {
    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin: 8px 16px;
    padding: 12px;
}

QWidget#messageContainer[sender="system"] {
    background-color: #f8f9fa;
    margin-left: 48px;  /* RTL support */
}

QWidget#messageContainer[sender="user"] {
    background-color: #e8f0fe;
    margin-right: 48px;  /* RTL support */
}

QLabel#messageSender {
    font-weight: 600;
    font-size: 13px;
    color: #202124;
    padding: 0 0 4px 0;
}

QLabel#messageContent {
    font-size: 14px;
    line-height: 1.5;
    color: #3c4043;
    padding: 0;
}

/* Input Area */
QWidget#inputPanel {
    background-color: #ffffff;
    border-top: 1px solid #e0e0e0;
    padding: 16px;
    margin: 0;
}

QTextEdit#messageInput {
    background-color: #f8f9fa;
    border: 1px solid #dadce0;
    border-radius: 24px;
    padding: 12px 16px;
    margin-right: 16px;  /* RTL support */
    font-size: 14px;
    min-height: 24px;
    max-height: 120px;
}

QTextEdit#messageInput:focus {
    border-color: #1a73e8;
    background-color: #ffffff;
}

QPushButton#sendButton {
    background-color: #1a73e8;
    color: #ffffff;
    border: none;
    border-radius: 24px;
    padding: 12px 24px;
    font-weight: 500;
    min-width: 96px;
    qproperty-layoutDirection: RightToLeft;  /* RTL support */
}

QPushButton#sendButton:hover {
    background-color: #1557b0;
}

QPushButton#sendButton:pressed {
    background-color: #174ea6;
}

QPushButton#sendButton:disabled {
    background-color: #dadce0;
    color: #9aa0a6;
}

QPushButton#sendButton:disabled:hover {
    background-color: #dadce0;
}

/* Progress Indicator */
QProgressBar {
    border: none;
    background-color: transparent;
    height: 2px;
    margin: 0;
    padding: 0;
}

QProgressBar::chunk {
    background-color: #1a73e8;
}

/* RTL Support - Use Qt Specific Properties */
/* RTL: alignments are handled in code (QLabel/QTextEdit alignment set via setAlignment or block format).
   Avoid qproperty-alignment for QTextEdit as it is not exposed as a stylesheet property and
   can emit runtime warnings. Layout direction is set in code as well. */

QMainWindow, QWidget {
    qproperty-layoutDirection: RightToLeft;
}
"""