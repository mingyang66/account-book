from PySide6.QtCore import QEvent, QPointF, QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPolygonF,
)
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


LOGIN_STYLE = """
QDialog#LoginDialog {
    background-color: #f3ead8;
}

QFrame#loginCard {
    background-color: #fffdf8;
    border: 1px solid #dfd3bd;
    border-radius: 22px;
}

QLabel#eyebrowLabel {
    color: #b45f43;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}

QLabel#titleLabel {
    color: #24463a;
    font-size: 30px;
    font-weight: bold;
}

QLabel#subtitleLabel {
    color: #7c7468;
    font-size: 13px;
}

QLabel#fieldLabel {
    color: #49443d;
    font-size: 12px;
    font-weight: bold;
}

QFrame#inputFrame {
    background-color: #faf6ed;
    border: 1px solid #d8ccb7;
    border-radius: 10px;
    min-height: 44px;
}

QFrame#inputFrame[active="true"] {
    background-color: #ffffff;
    border: 1px solid #42755f;
}

QFrame#inputFrame[error="true"] {
    background-color: #fff8f5;
    border: 1px solid #c95e4a;
}

QLineEdit {
    background-color: transparent;
    border: none;
    color: #292621;
    font-size: 14px;
    padding: 0 8px;
    selection-background-color: #8cab7d;
}

QPushButton#passwordToggle {
    background-color: transparent;
    border: none;
    color: #6f796f;
    font-size: 12px;
    min-width: 42px;
    padding: 7px 8px;
}

QPushButton#passwordToggle:hover {
    color: #2f6651;
}

QLabel#errorLabel {
    color: #bd4f3d;
    font-size: 12px;
    min-height: 18px;
}

QPushButton#loginButton {
    background-color: #315f4c;
    color: #fffdf7;
    border: none;
    border-radius: 11px;
    min-height: 46px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 3px;
}

QPushButton#loginButton:hover {
    background-color: #3d745d;
}

QPushButton#loginButton:pressed {
    background-color: #244c3c;
}

QPushButton#loginButton:focus {
    border: 2px solid #9eb49c;
}

QLabel#tipLabel {
    color: #948a7b;
    font-size: 11px;
}
"""


class FieldIcon(QWidget):
    """Small line icon that follows the storefront palette."""

    def __init__(self, icon_type, parent=None):
        super().__init__(parent)
        self.icon_type = icon_type
        self.setFixedSize(28, 28)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("#547064"), 1.7, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)

        if self.icon_type == "user":
            painter.drawEllipse(QRectF(10, 5, 8, 8))
            painter.drawArc(QRectF(6.5, 14, 15, 11), 0, 180 * 16)
        else:
            painter.drawEllipse(QRectF(5, 8, 9, 9))
            painter.drawLine(QPointF(13, 14), QPointF(22, 14))
            painter.drawLine(QPointF(19, 14), QPointF(19, 18))
            painter.drawLine(QPointF(22, 14), QPointF(22, 17))


class StorefrontIllustration(QWidget):
    """Resource-free storefront artwork that scales cleanly on HiDPI screens."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        painter.translate((width - 350) / 2, (height - 430) / 2)

        # Soft sun and ground keep the illustration from looking like a flat icon.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 246, 212, 150))
        painter.drawEllipse(QRectF(18, 12, 290, 290))
        painter.setBrush(QColor("#d8cfb8"))
        painter.drawEllipse(QRectF(31, 391, 288, 18))

        # Roof, shop body and sign board.
        painter.setBrush(QColor("#315f4c"))
        painter.drawPolygon(QPolygonF([
            QPointF(54, 120), QPointF(175, 45), QPointF(296, 120)
        ]))
        painter.setBrush(QColor("#fffaf0"))
        painter.drawRoundedRect(QRectF(61, 115, 228, 280), 8, 8)

        painter.setBrush(QColor("#f4d99b"))
        painter.drawRoundedRect(QRectF(103, 74, 144, 54), 9, 9)
        painter.setPen(QPen(QColor("#315f4c"), 2))
        painter.drawRoundedRect(QRectF(103, 74, 144, 54), 9, 9)
        painter.setFont(QFont("Microsoft YaHei", 15, QFont.Bold))
        painter.drawText(QRectF(103, 74, 144, 54), Qt.AlignCenter, "小妖杂货铺")

        # Striped awning.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#b85f45"))
        painter.drawRoundedRect(QRectF(45, 137, 260, 50), 7, 7)
        painter.setBrush(QColor("#f5d895"))
        for x in range(71, 280, 52):
            painter.drawRect(QRectF(x, 137, 26, 50))
        painter.setBrush(QColor("#fffaf0"))
        painter.drawRect(QRectF(61, 177, 228, 12))

        # Window, shelves and jars.
        painter.setBrush(QColor("#b9d6cc"))
        painter.drawRoundedRect(QRectF(80, 210, 108, 119), 4, 4)
        painter.setPen(QPen(QColor("#315f4c"), 4))
        painter.drawRect(QRectF(80, 210, 108, 119))
        painter.drawLine(QPointF(134, 211), QPointF(134, 329))
        painter.drawLine(QPointF(82, 269), QPointF(186, 269))

        painter.setPen(Qt.NoPen)
        jar_colors = ["#cf7456", "#e6b85d", "#6f947b"]
        for index, color in enumerate(jar_colors):
            x = 91 + index * 29
            painter.setBrush(QColor(color))
            painter.drawRoundedRect(QRectF(x, 236, 20, 25), 4, 4)
            painter.setBrush(QColor("#f8ecd0"))
            painter.drawRect(QRectF(x + 3, 232, 14, 5))

        # Door with a warm lamp and tiny welcome sign.
        painter.setBrush(QColor("#8e543f"))
        painter.drawRoundedRect(QRectF(207, 210, 62, 185), 4, 4)
        painter.setBrush(QColor("#f4d99b"))
        painter.drawRoundedRect(QRectF(216, 226, 44, 67), 3, 3)
        painter.setBrush(QColor("#dcae56"))
        painter.drawEllipse(QRectF(249, 307, 7, 7))
        painter.setBrush(QColor("#fff7df"))
        painter.drawRoundedRect(QRectF(214, 331, 48, 31), 4, 4)
        painter.setPen(QColor("#604c3d"))
        painter.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        painter.drawText(QRectF(214, 331, 48, 31), Qt.AlignCenter, "营业中")

        # A few plants make the storefront feel lived-in.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#a95c42"))
        painter.drawRoundedRect(QRectF(43, 358, 40, 37), 3, 3)
        painter.setBrush(QColor("#5b8268"))
        for rect in (
            QRectF(39, 330, 25, 39), QRectF(57, 320, 23, 48),
            QRectF(69, 338, 21, 32),
        ):
            painter.drawEllipse(rect)


class LoginDialog(QDialog):
    Accepted = QDialog.DialogCode.Accepted

    def __init__(self, auth_service, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.password_visible = False

        self.setObjectName("LoginDialog")
        self.setWindowTitle("小妖杂货铺 - 店主登录")
        self.setFixedSize(860, 560)
        self.setStyleSheet(LOGIN_STYLE)
        self.setup_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#f5eddd"))
        gradient.setColorAt(1, QColor("#e6dbc5"))
        painter.fillRect(self.rect(), gradient)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(49, 95, 76, 18))
        painter.drawEllipse(QRectF(-90, 355, 330, 260))
        painter.setBrush(QColor(184, 95, 69, 18))
        painter.drawEllipse(QRectF(680, -100, 270, 270))

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(42, 36, 42, 36)
        main_layout.setSpacing(42)

        illustration = StorefrontIllustration()
        illustration.setMinimumWidth(390)
        main_layout.addWidget(illustration, 1)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(350)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(34, 34, 34, 30)
        card_layout.setSpacing(0)

        eyebrow = QLabel("SHOPKEEPER  ·  LOGIN")
        eyebrow.setObjectName("eyebrowLabel")
        card_layout.addWidget(eyebrow)
        card_layout.addSpacing(8)

        title = QLabel("欢迎回来")
        title.setObjectName("titleLabel")
        card_layout.addWidget(title)
        card_layout.addSpacing(5)

        subtitle = QLabel("登录后继续打理你的每一笔账目")
        subtitle.setObjectName("subtitleLabel")
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(27)

        username_label = QLabel("店主账号")
        username_label.setObjectName("fieldLabel")
        card_layout.addWidget(username_label)
        card_layout.addSpacing(7)

        self.username_frame, self.username_input = self.create_input("user")
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setFocusPolicy(Qt.StrongFocus)
        self.username_input.textChanged.connect(self.clear_username_error)
        card_layout.addWidget(self.username_frame)
        card_layout.addSpacing(16)

        password_label = QLabel("通行口令")
        password_label.setObjectName("fieldLabel")
        card_layout.addWidget(password_label)
        card_layout.addSpacing(7)

        self.password_frame, self.password_input = self.create_input("key")
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.on_login)
        self.password_input.textChanged.connect(self.clear_password_error)

        self.password_toggle = QPushButton("显示")
        self.password_toggle.setObjectName("passwordToggle")
        self.password_toggle.setCursor(Qt.PointingHandCursor)
        self.password_toggle.setFocusPolicy(Qt.NoFocus)
        self.password_toggle.clicked.connect(self.toggle_password_visibility)
        self.password_frame.layout().addWidget(self.password_toggle)
        card_layout.addWidget(self.password_frame)
        card_layout.addSpacing(5)

        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        card_layout.addWidget(self.error_label)
        card_layout.addSpacing(8)

        login_button = QPushButton("进入店铺")
        login_button.setObjectName("loginButton")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.on_login)
        card_layout.addWidget(login_button)
        card_layout.addStretch()

        tip = QLabel("认真记下日常，也收藏生活的小确幸")
        tip.setObjectName("tipLabel")
        tip.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(tip)

        main_layout.addWidget(card)
        self.username_input.setFocus()

    def create_input(self, icon_type):
        frame = QFrame()
        frame.setObjectName("inputFrame")
        frame.setProperty("active", False)
        frame.setProperty("error", False)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 2, 8, 2)
        layout.setSpacing(3)
        layout.addWidget(FieldIcon(icon_type))

        line_edit = QLineEdit()
        line_edit.installEventFilter(self)
        layout.addWidget(line_edit)
        return frame, line_edit

    def eventFilter(self, watched, event):
        username_input = getattr(self, "username_input", None)
        password_input = getattr(self, "password_input", None)
        if watched in (username_input, password_input):
            if event.type() in (QEvent.FocusIn, QEvent.FocusOut):
                frame = (
                    self.username_frame
                    if watched is username_input
                    else self.password_frame
                )
                frame.setProperty("active", event.type() == QEvent.FocusIn)
                self.refresh_style(frame)
        return super().eventFilter(watched, event)

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        echo_mode = QLineEdit.Normal if self.password_visible else QLineEdit.Password
        self.password_input.setEchoMode(echo_mode)
        self.password_toggle.setText("隐藏" if self.password_visible else "显示")

    @staticmethod
    def refresh_style(widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()

    def set_error(self, frame, message):
        frame.setProperty("error", True)
        self.refresh_style(frame)
        self.error_label.setText(message)

    def clear_error(self, frame):
        if frame.property("error"):
            frame.setProperty("error", False)
            self.refresh_style(frame)
        if not self.username_frame.property("error") and not self.password_frame.property("error"):
            self.error_label.clear()

    def clear_username_error(self):
        self.clear_error(self.username_frame)

    def clear_password_error(self):
        self.clear_error(self.password_frame)

    def on_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            self.set_error(self.username_frame, "请填写店主账号")
            self.username_input.setFocus()
            return

        if not password:
            self.set_error(self.password_frame, "请填写通行口令")
            self.password_input.setFocus()
            return

        if self.auth_service.login(username, password):
            self.accept()
            return

        self.password_input.clear()
        self.username_frame.setProperty("error", True)
        self.password_frame.setProperty("error", True)
        self.refresh_style(self.username_frame)
        self.refresh_style(self.password_frame)
        self.error_label.setText("账号或口令不正确，请重新检查")
        self.password_input.setFocus()
