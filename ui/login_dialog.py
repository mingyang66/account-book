from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QEasingCurve
from PySide6.QtGui import QFont, QLinearGradient, QPainter, QColor


# 登录页面专用样式
LOGIN_STYLE = """
QDialog#LoginDialog {
    background-color: transparent;
}

QFrame#cardFrame {
    background-color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 16px;
    padding: 20px;
}

QLabel#titleLabel {
    color: #1890ff;
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 2px;
}

QLabel#subtitleLabel {
    color: #8c8c8c;
    font-size: 13px;
}

QFrame#inputFrame {
    background-color: #ffffff;
    border: 2px solid #d9d9d9;
    border-radius: 10px;
    padding: 0 8px;
    min-height: 42px;
}

QFrame#inputFrame[error="true"] {
    border: 2px solid #ff4d4f;
}

QFrame#inputFrame[error="true"] QLineEdit {
    color: #ff4d4f;
}

QLineEdit {
    background-color: transparent;
    border: none;
    color: #1a1a1a;
    font-size: 15px;
    padding: 4px 14px;
}

QLabel#iconLabel {
    background-color: transparent;
    padding: 0 4px 0 8px;
}

QPushButton#pwdToggleBtn {
    background-color: transparent;
    border: none;
    color: #8c8c8c;
    font-size: 18px;
    padding: 4px 8px;
    min-width: 32px;
    max-width: 32px;
}

QPushButton#pwdToggleBtn:hover {
    color: #1890ff;
}

QPushButton#loginBtn {
    background-color: #1890ff;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    min-height: 48px;
    letter-spacing: 2px;
}

QPushButton#loginBtn:hover {
    background-color: #40a9ff;
}

QPushButton#loginBtn:pressed {
    background-color: #096dd9;
}

QPushButton#loginBtn:focus {
    background-color: #1890ff;
}

QLabel#footerLabel {
    color: rgba(255, 255, 255, 0.6);
    font-size: 11px;
}
"""


class LoginDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("小妖记账 - 登录")
        self.setFixedSize(440, 560)
        
        # 设置对象名称，用于样式选择器
        self.setObjectName("LoginDialog")
        
        # 应用登录页面专用样式
        self.setStyleSheet(LOGIN_STYLE)
        
        # 设置窗口标志，确保背景透明生效
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.setup_ui()
        self.password_visible = False

    def paintEvent(self, event):
        # 绘制渐变背景
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(1, QColor("#764ba2"))
        
        painter.fillRect(self.rect(), gradient)

    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 50, 40, 30)
        main_layout.setSpacing(0)
        
        # 顶部 Logo 区域
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.setSpacing(12)
        
        logo_icon = QLabel("💰")
        logo_icon.setFont(QFont("", 56))
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("background-color: transparent; color: white;")
        logo_layout.addWidget(logo_icon)
        
        title_label = QLabel("小妖记账")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(title_label)
        
        subtitle_label = QLabel("欢迎使用个人财务管理")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(subtitle_label)
        
        logo_layout.addSpacing(24)
        main_layout.addLayout(logo_layout)
        
        # 白色卡片登录表单
        card_frame = QFrame()
        card_frame.setObjectName("cardFrame")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(24, 32, 24, 32)
        card_layout.setSpacing(50)
        
        # 用户名输入区域
        self.username_frame = QFrame()
        self.username_frame.setObjectName("inputFrame")
        username_layout = QHBoxLayout(self.username_frame)
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_layout.setSpacing(0)
        
        username_icon = QLabel("👤")
        username_icon.setObjectName("iconLabel")
        username_icon.setFont(QFont("", 12))
        username_layout.addWidget(username_icon)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名...")
        self.username_input.setFont(QFont("", 12))
        self.username_input.setFocusPolicy(Qt.StrongFocus)
        self.username_input.textChanged.connect(self.clear_username_error)
        username_layout.addWidget(self.username_input)
        
        card_layout.addWidget(self.username_frame)
        
        # 密码输入区域
        self.password_frame = QFrame()
        self.password_frame.setObjectName("inputFrame")
        password_layout = QHBoxLayout(self.password_frame)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)
        
        password_icon = QLabel("🔒")
        password_icon.setObjectName("iconLabel")
        password_icon.setFont(QFont("", 14))
        password_layout.addWidget(password_icon)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码...")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("", 13))
        self.password_input.returnPressed.connect(self.on_login)
        self.password_input.textChanged.connect(self.clear_password_error)
        password_layout.addWidget(self.password_input)
        
        # 密码显示切换按钮
        self.pwd_toggle_btn = QPushButton("👁")
        self.pwd_toggle_btn.setObjectName("pwdToggleBtn")
        self.pwd_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.pwd_toggle_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.pwd_toggle_btn)
        
        card_layout.addWidget(self.password_frame)
        
        # 添加间距
        card_layout.addSpacing(12)
        
        # 登录按钮
        login_btn = QPushButton("登 录")
        login_btn.setObjectName("loginBtn")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.on_login)
        card_layout.addWidget(login_btn)
        
        main_layout.addWidget(card_frame)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        # 底部页脚
        footer_label = QLabel("© 2026 Account Book  |  版本 1.0")
        footer_label.setObjectName("footerLabel")
        footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer_label)
        
        # 设置焦点到用户名输入框
        self.username_input.setFocus()

    def toggle_password_visibility(self):
        """切换密码显示/隐藏"""
        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.pwd_toggle_btn.setText("👁")
            self.password_visible = False
        else:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.pwd_toggle_btn.setText("🙈")
            self.password_visible = True

    def shake_frame(self, frame):
        """对输入框执行抖动动画"""
        original_pos = frame.pos().x()
        anim = QSequentialAnimationGroup(frame)
        
        offsets = [-12, 10, -8, 6, -4, 2, 0]
        for offset in offsets:
            a = QPropertyAnimation(frame, b"pos")
            a.setDuration(50)
            a.setEasingCurve(QEasingCurve.OutQuad)
            a.setStartValue(frame.pos())
            a.setEndValue(frame.pos() + type(frame.pos())(offset, 0))
            anim.addAnimation(a)
        
        anim.start()
        self._shake_anim = anim

    def set_error(self, frame):
        """设置输入框错误状态"""
        frame.setProperty("error", True)
        frame.style().unpolish(frame)
        frame.style().polish(frame)
        self.shake_frame(frame)

    def clear_error(self, frame):
        """清除输入框错误状态"""
        frame.setProperty("error", False)
        frame.style().unpolish(frame)
        frame.style().polish(frame)

    def clear_username_error(self):
        self.clear_error(self.username_frame)

    def clear_password_error(self):
        self.clear_error(self.password_frame)

    def on_login(self):
        """登录处理"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username:
            self.set_error(self.username_frame)
            self.username_input.setFocus()
            return
        
        if not password:
            self.set_error(self.password_frame)
            self.password_input.setFocus()
            return
        
        if self.db.verify_account(username, password):
            self.accept()
        else:
            self.set_error(self.username_frame)
            self.set_error(self.password_frame)
            self.password_input.clear()
            self.password_input.setFocus()
