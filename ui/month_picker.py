from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QButtonGroup, QDialog, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout
)


MONTH_PICKER_STYLE = """
QDialog#monthPickerDialog {
    background-color: #ffffff;
}

QLabel#monthPickerTitle {
    color: #1a1a1a;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#yearNavButton {
    background-color: #ffffff;
    color: #1890ff;
    border: 1px solid #d9e8f5;
    border-radius: 6px;
    min-width: 34px;
    min-height: 32px;
    font-size: 17px;
    font-weight: bold;
}

QPushButton#yearNavButton:hover {
    background-color: #e6f7ff;
    border-color: #40a9ff;
}

QLabel#selectedYearLabel {
    color: #1a1a1a;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#monthButton {
    background-color: #f7f9fc;
    color: #595959;
    border: 1px solid #edf0f5;
    border-radius: 8px;
    min-width: 68px;
    min-height: 42px;
    font-size: 13px;
}

QPushButton#monthButton:hover {
    background-color: #e6f7ff;
    border-color: #91d5ff;
    color: #1890ff;
}

QPushButton#monthButton:checked {
    background-color: #1890ff;
    border-color: #1890ff;
    color: #ffffff;
    font-weight: bold;
}

QPushButton#currentMonthButton {
    background-color: transparent;
    color: #1890ff;
    border: none;
    padding: 8px 12px;
    font-size: 13px;
}

QPushButton#currentMonthButton:hover {
    background-color: #e6f7ff;
    border-radius: 6px;
}

QPushButton#monthPickerCancel {
    background-color: #ffffff;
    color: #595959;
    border: 1px solid #d9d9d9;
    border-radius: 6px;
    padding: 8px 20px;
}

QPushButton#monthPickerCancel:hover {
    border-color: #1890ff;
    color: #1890ff;
}

QPushButton#monthPickerConfirm {
    background-color: #1890ff;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 22px;
    font-weight: bold;
}

QPushButton#monthPickerConfirm:hover {
    background-color: #40a9ff;
}
"""


class MonthPickerDialog(QDialog):
    def __init__(self, year, month, parent=None):
        super().__init__(parent)
        self._year = year
        self._month = month
        self.setObjectName("monthPickerDialog")
        self.setWindowTitle("选择统计周期")
        self.setFixedSize(390, 330)
        self.setStyleSheet(MONTH_PICKER_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(16)

        title = QLabel("选择统计周期")
        title.setObjectName("monthPickerTitle")
        layout.addWidget(title)

        year_row = QHBoxLayout()
        previous_button = QPushButton("<")
        previous_button.setObjectName("yearNavButton")
        previous_button.setCursor(Qt.PointingHandCursor)
        previous_button.clicked.connect(lambda: self.change_year(-1))
        year_row.addWidget(previous_button)
        year_row.addStretch()
        self.year_label = QLabel()
        self.year_label.setObjectName("selectedYearLabel")
        self.year_label.setAlignment(Qt.AlignCenter)
        year_row.addWidget(self.year_label)
        year_row.addStretch()
        next_button = QPushButton(">")
        next_button.setObjectName("yearNavButton")
        next_button.setCursor(Qt.PointingHandCursor)
        next_button.clicked.connect(lambda: self.change_year(1))
        year_row.addWidget(next_button)
        layout.addLayout(year_row)

        months_grid = QGridLayout()
        months_grid.setHorizontalSpacing(10)
        months_grid.setVerticalSpacing(10)
        self.month_group = QButtonGroup(self)
        self.month_group.setExclusive(True)
        self.month_buttons = []
        for month_number in range(1, 13):
            button = QPushButton(f"{month_number}月")
            button.setObjectName("monthButton")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(
                lambda checked, value=month_number: self.select_month(value)
            )
            self.month_group.addButton(button, month_number)
            self.month_buttons.append(button)
            months_grid.addWidget(button, (month_number - 1) // 4, (month_number - 1) % 4)
        layout.addLayout(months_grid)

        actions = QHBoxLayout()
        current_button = QPushButton("本月")
        current_button.setObjectName("currentMonthButton")
        current_button.setCursor(Qt.PointingHandCursor)
        current_button.clicked.connect(self.select_current_month)
        actions.addWidget(current_button)
        actions.addStretch()
        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("monthPickerCancel")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)
        actions.addWidget(cancel_button)
        confirm_button = QPushButton("确定")
        confirm_button.setObjectName("monthPickerConfirm")
        confirm_button.setCursor(Qt.PointingHandCursor)
        confirm_button.clicked.connect(self.accept)
        actions.addWidget(confirm_button)
        layout.addLayout(actions)

        self._refresh_selection()

    def change_year(self, offset):
        self._year += offset
        self._refresh_selection()

    def select_month(self, month):
        self._month = month
        self._refresh_selection()

    def select_current_month(self):
        today = QDate.currentDate()
        self._year = today.year()
        self._month = today.month()
        self._refresh_selection()

    def selected_year(self):
        return self._year

    def selected_month(self):
        return self._month

    def _refresh_selection(self):
        self.year_label.setText(f"{self._year}年")
        for index, button in enumerate(self.month_buttons, start=1):
            button.setChecked(index == self._month)


class MonthPicker(QPushButton):
    def __init__(self, year=None, month=None, parent=None):
        super().__init__(parent)
        today = QDate.currentDate()
        self._year = year or today.year()
        self._month = month or today.month()
        self.setObjectName("monthPicker")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.clicked.connect(self.open_picker)
        self._update_text()

    def open_picker(self):
        dialog = MonthPickerDialog(self._year, self._month, self)
        if dialog.exec() == QDialog.Accepted:
            self.set_period(dialog.selected_year(), dialog.selected_month())

    def set_period(self, year, month):
        if 1 <= month <= 12:
            self._year = year
            self._month = month
            self._update_text()

    def year(self):
        return self._year

    def month(self):
        return self._month

    def _update_text(self):
        self.setText(f"📅  {self._year}年{self._month:02d}月")
