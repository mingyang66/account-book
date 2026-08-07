from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AccountDialog(QDialog):
    def __init__(self, db, username, parent=None):
        super().__init__(parent)
        self.db = db
        self.username = username
        self.setWindowTitle("修改密码")
        self.setFixedSize(420, 350)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(16)

        title = QLabel("修改密码")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1890ff;")
        layout.addWidget(title)

        layout.addSpacing(8)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        user_label = QLabel(self.username)
        user_label.setFont(QFont("Microsoft YaHei", 11))
        user_label.setStyleSheet("color: #1a1a1a; padding: 4px 0;")
        form.addRow(self.create_form_label("账号:"), user_label)

        self.old_pwd_input = QLineEdit()
        self.old_pwd_input.setPlaceholderText("请输入原密码")
        self.old_pwd_input.setEchoMode(QLineEdit.Password)
        self.old_pwd_input.setFont(QFont("Microsoft YaHei", 10))
        self.old_pwd_input.setMinimumHeight(32)
        form.addRow(self.create_form_label("原密码:"), self.old_pwd_input)

        self.new_pwd_input = QLineEdit()
        self.new_pwd_input.setPlaceholderText("请输入新密码（至少6位）")
        self.new_pwd_input.setEchoMode(QLineEdit.Password)
        self.new_pwd_input.setFont(QFont("Microsoft YaHei", 10))
        self.new_pwd_input.setMinimumHeight(32)
        form.addRow(self.create_form_label("新密码:"), self.new_pwd_input)

        self.confirm_pwd_input = QLineEdit()
        self.confirm_pwd_input.setPlaceholderText("请再次输入新密码")
        self.confirm_pwd_input.setEchoMode(QLineEdit.Password)
        self.confirm_pwd_input.setFont(QFont("Microsoft YaHei", 10))
        self.confirm_pwd_input.setMinimumHeight(32)
        self.confirm_pwd_input.returnPressed.connect(self.on_save)
        form.addRow(self.create_form_label("确认密码:"), self.confirm_pwd_input)

        layout.addLayout(form)
        layout.addSpacing(16)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont("Microsoft YaHei", 10))
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #595959;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        save_btn.setMinimumHeight(36)
        save_btn.setMinimumWidth(100)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def create_form_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Microsoft YaHei", 10))
        label.setStyleSheet("color: #595959;")
        label.setMinimumWidth(80)
        return label

    def on_save(self):
        old_pwd = self.old_pwd_input.text().strip()
        new_pwd = self.new_pwd_input.text().strip()
        confirm_pwd = self.confirm_pwd_input.text().strip()

        if not old_pwd:
            QMessageBox.warning(self, "提示", "请输入原密码")
            self.old_pwd_input.setFocus()
            return

        if not new_pwd:
            QMessageBox.warning(self, "提示", "请输入新密码")
            self.new_pwd_input.setFocus()
            return

        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, "提示", "两次密码输入不一致")
            self.confirm_pwd_input.clear()
            self.confirm_pwd_input.setFocus()
            return

        success, message = self.db.change_password(self.username, old_pwd, new_pwd)
        if success:
            QMessageBox.information(self, "提示", message)
            self.accept()
        else:
            QMessageBox.critical(self, "修改失败", message)
            self.old_pwd_input.clear()
            self.old_pwd_input.setFocus()


class AccountFormDialog(QDialog):
    def __init__(self, db, account=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.account = account
        self.setWindowTitle("新增账号" if account is None else "编辑账号")
        self.setFixedSize(420, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(16)

        title = QLabel("新增账号" if self.account is None else "编辑账号")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1890ff;")
        layout.addWidget(title)

        layout.addSpacing(8)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setFont(QFont("Microsoft YaHei", 10))
        self.username_input.setMinimumHeight(32)
        form.addRow(self.create_form_label("用户名:"), self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码（至少6位）")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Microsoft YaHei", 10))
        self.password_input.setMinimumHeight(32)
        form.addRow(self.create_form_label("密码:"), self.password_input)

        layout.addLayout(form)
        layout.addSpacing(16)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont("Microsoft YaHei", 10))
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #595959;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        save_btn.setMinimumHeight(36)
        save_btn.setMinimumWidth(100)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

        if self.account:
            self.username_input.setText(self.account['username'])
            self.password_input.setText(self.account['password'])

    def create_form_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Microsoft YaHei", 10))
        label.setStyleSheet("color: #595959;")
        label.setMinimumWidth(80)
        return label

    def on_save(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            QMessageBox.warning(self, "提示", "请输入用户名")
            self.username_input.setFocus()
            return

        if not password or len(password) < 6:
            QMessageBox.warning(self, "提示", "密码不能少于6位")
            self.password_input.setFocus()
            return

        if self.account is None:
            success, message = self.db.add_account(username, password)
        else:
            success, message = self.db.update_account(self.account['id'], username, password)

        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "错误", message)
