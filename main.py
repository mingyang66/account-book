import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from styles import MAIN_STYLE
from database import Database
from session import UserSession
from security import PasswordHasher
from services import AccountService, AuthService, TransactionService


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(MAIN_STYLE)

    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    database = Database()
    password_hasher = PasswordHasher()
    account_service = AccountService(database, password_hasher)

    try:
        while True:
            session = UserSession()
            auth_service = AuthService(database, password_hasher, session)
            transaction_service = TransactionService(database, session)
            #创建登录提示框对象
            login_dialog = LoginDialog(auth_service)
            if login_dialog.exec() != LoginDialog.Accepted:
                break

            #创建主应用程序窗口
            window = MainWindow(
                transaction_service,
                account_service,
                auth_service,
                session,
            )
            window.show()
            app.exec()
            #获取window对象的_logged_out属性，不存在则使用False，用户点击退出会设置为True
            logged_out = getattr(window, '_logged_out', False)
            window.close()
            auth_service.logout()

            if not logged_out:
                break
    finally:
        database.close()


if __name__ == "__main__":
    main()
