import sys
import os
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from styles import MAIN_STYLE
from database import Database


def install_libpng_warning_filter():
    """Filter only the known harmless libpng iCCP warning from native stderr."""
    ignored_warning = b"libpng warning: iCCP: known incorrect sRGB profile"
    read_fd, write_fd = os.pipe()
    original_stderr = os.dup(2)
    os.dup2(write_fd, 2)
    os.close(write_fd)

    def forward_stderr():
        pending = b""
        while True:
            chunk = os.read(read_fd, 4096)
            if not chunk:
                break
            pending += chunk
            while b"\n" in pending:
                line, pending = pending.split(b"\n", 1)
                if ignored_warning not in line:
                    os.write(original_stderr, line + b"\n")
        if pending and ignored_warning not in pending:
            os.write(original_stderr, pending)
        os.close(read_fd)

    thread = threading.Thread(target=forward_stderr, daemon=True)
    thread.start()

    def cleanup():
        sys.stderr.flush()
        os.dup2(original_stderr, 2)
        os.close(original_stderr)
        thread.join(timeout=0.2)

    return cleanup


def main():
    cleanup_stderr = install_libpng_warning_filter()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(MAIN_STYLE)

    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    try:
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
    finally:
        cleanup_stderr()


if __name__ == "__main__":
    main()
