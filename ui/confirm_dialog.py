from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
)


CONFIRM_DIALOG_STYLE = """
QDialog#confirmDialog {
    background-color: #ffffff;
}

QLabel#confirmIcon {
    background-color: #fff7e6;
    color: #fa8c16;
    border: 1px solid #ffd591;
    border-radius: 23px;
    font-size: 22px;
    font-weight: bold;
}

QLabel#confirmTitle {
    color: #1a1a1a;
    font-size: 17px;
    font-weight: bold;
}

QLabel#confirmMessage {
    color: #595959;
    font-size: 13px;
}

QLabel#confirmDescription {
    color: #8c8c8c;
    font-size: 12px;
}

QPushButton#confirmCancelButton {
    background-color: #ffffff;
    color: #595959;
    border: 1px solid #d9d9d9;
    border-radius: 7px;
    padding: 0 20px;
    min-width: 72px;
    min-height: 38px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#confirmCancelButton:hover,
QPushButton#confirmCancelButton:focus {
    background-color: #f5f5f5;
    border-color: #8c8c8c;
    color: #1a1a1a;
}

QPushButton#confirmDangerButton {
    background-color: #ff4d4f;
    color: #ffffff;
    border: 1px solid #ff4d4f;
    border-radius: 7px;
    padding: 0 20px;
    min-width: 92px;
    min-height: 38px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#confirmDangerButton:hover {
    background-color: #ff7875;
    border-color: #ff7875;
}

QPushButton#confirmDangerButton:pressed {
    background-color: #cf1322;
    border-color: #cf1322;
}
"""


class ConfirmDialog(QDialog):
    def __init__(
        self, title, message, description="", confirm_text="确定", parent=None
    ):
        super().__init__(parent)
        self.setObjectName("confirmDialog")
        self.setWindowTitle(title)
        self.setFixedSize(390, 270)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(CONFIRM_DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(10)

        icon = QLabel("!")
        icon.setObjectName("confirmIcon")
        icon.setFixedSize(54, 54)
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon, 0, Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setObjectName("confirmTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        message_label = QLabel(message)
        message_label.setObjectName("confirmMessage")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        if description:
            description_label = QLabel(description)
            description_label.setObjectName("confirmDescription")
            description_label.setAlignment(Qt.AlignCenter)
            description_label.setWordWrap(True)
            layout.addWidget(description_label)

        layout.addStretch()

        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addStretch()
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("confirmCancelButton")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        actions.addWidget(self.cancel_button)

        self.confirm_button = QPushButton(confirm_text)
        self.confirm_button.setObjectName("confirmDangerButton")
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.clicked.connect(self.accept)
        actions.addWidget(self.confirm_button)
        actions.addStretch()
        layout.addLayout(actions)

        self.cancel_button.setDefault(True)
        self.cancel_button.setFocus()

    @classmethod
    def ask(
        cls, parent, title, message, description="", confirm_text="确定"
    ):
        dialog = cls(title, message, description, confirm_text, parent)
        return dialog.exec() == QDialog.Accepted
