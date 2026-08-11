"""应用程序入口和依赖组装模块。

本模块负责初始化 Qt、创建数据库与 Service，并控制“登录 -> 主窗口 ->
退出登录后重新登录”的应用生命周期。具体业务逻辑由 Service 层处理。
"""

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
    """初始化应用并运行登录及主窗口事件循环。"""
    # QApplication 是所有 Qt 控件和事件循环的入口，整个进程只能创建一个。
    app = QApplication(sys.argv)
    # Fusion 在不同 Windows 版本上提供较统一的基础控件外观。
    app.setStyle("Fusion")
    app.setStyleSheet(MAIN_STYLE)

    # 设置应用级默认字体，单个控件仍可通过 QFont 或 QSS 覆盖。
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    # 数据库连接和无状态依赖在应用周期内复用，避免每次重登重复创建。
    database = Database()
    password_hasher = PasswordHasher()
    account_service = AccountService(database, password_hasher)

    try:
        # 用户主动退出登录时继续下一轮；关闭主窗口或取消登录时结束循环。
        while True:
            # 会话包含当前用户状态，因此每轮登录都创建新的独立对象。
            session = UserSession()
            auth_service = AuthService(database, password_hasher, session)
            transaction_service = TransactionService(database, session)

            # LoginDialog 只调用认证服务；登录成功后会话已经写入用户信息。
            login_dialog = LoginDialog(auth_service)
            if login_dialog.exec() != LoginDialog.Accepted:
                break

            # 主窗口通过 Service 操作业务，不直接访问数据库或密码组件。
            window = MainWindow(
                transaction_service,
                account_service,
                auth_service,
                session,
            )
            window.show()
            app.exec()

            # True 表示用户选择“退出登录”；False 表示直接关闭整个应用。
            logged_out = getattr(window, '_logged_out', False)
            window.close()
            auth_service.logout()

            if not logged_out:
                break
    finally:
        # 无论正常退出还是发生异常，都确保释放 SQLite 连接。
        database.close()


if __name__ == "__main__":
    # 仅直接运行 main.py 时启动应用，被其他模块导入时不自动执行。
    main()
