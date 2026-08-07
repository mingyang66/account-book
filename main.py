import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from styles import MAIN_STYLE
from database import Database


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(MAIN_STYLE)

    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    while True:
        db = Database()

        login_dialog = LoginDialog(db)
        if login_dialog.exec() != LoginDialog.Accepted:
            db.close()
            break

        username = login_dialog.username_input.text().strip()

        window = MainWindow(db, username)
        window.show()
        app.exec()

        logged_out = getattr(window, '_logged_out', False)
        window.close()
        db.close()

        if not logged_out:
            break


if __name__ == "__main__":
    main()
