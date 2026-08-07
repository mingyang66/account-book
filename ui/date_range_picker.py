from PySide6.QtCore import QDate, QLocale, Qt
from PySide6.QtWidgets import (
    QCalendarWidget, QDialog, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget
)


DATE_RANGE_STYLE = """
QDialog#dateRangeDialog {
    background-color: #ffffff;
}

QLabel#dateRangeTitle {
    color: #1a1a1a;
    font-size: 16px;
    font-weight: bold;
}

QLabel#calendarTitle {
    color: #595959;
    font-size: 13px;
    font-weight: bold;
}

QFrame#shortcutBar {
    background-color: #f7f9fc;
    border: 1px solid #edf0f5;
    border-radius: 8px;
}

QPushButton#shortcutButton {
    background-color: transparent;
    color: #595959;
    border: none;
    border-radius: 6px;
    padding: 7px 14px;
    font-size: 13px;
}

QPushButton#shortcutButton:hover {
    background-color: #e6f7ff;
    color: #1890ff;
}

QCalendarWidget {
    background-color: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #f7f9fc;
    border-bottom: 1px solid #edf0f5;
}

QCalendarWidget QToolButton {
    color: #1a1a1a;
    background-color: transparent;
    border: none;
    border-radius: 5px;
    padding: 6px;
    font-weight: bold;
}

QCalendarWidget QToolButton:hover {
    background-color: #e6f7ff;
    color: #1890ff;
}

QCalendarWidget QAbstractItemView {
    color: #595959;
    selection-background-color: #1890ff;
    selection-color: #ffffff;
    outline: none;
}

QPushButton#dateRangeCancel {
    background-color: #ffffff;
    color: #595959;
    border: 1px solid #d9d9d9;
    border-radius: 6px;
    padding: 8px 20px;
}

QPushButton#dateRangeCancel:hover {
    border-color: #1890ff;
    color: #1890ff;
}

QPushButton#dateRangeConfirm {
    background-color: #1890ff;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 22px;
    font-weight: bold;
}

QPushButton#dateRangeConfirm:hover {
    background-color: #40a9ff;
}
"""


class DateRangeDialog(QDialog):
    def __init__(self, start_date, end_date, parent=None):
        super().__init__(parent)
        self.setObjectName("dateRangeDialog")
        self.setWindowTitle("选择日期范围")
        self.setFixedSize(700, 430)
        self.setStyleSheet(DATE_RANGE_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        title = QLabel("选择日期范围")
        title.setObjectName("dateRangeTitle")
        layout.addWidget(title)

        shortcut_bar = QFrame()
        shortcut_bar.setObjectName("shortcutBar")
        shortcut_layout = QHBoxLayout(shortcut_bar)
        shortcut_layout.setContentsMargins(8, 6, 8, 6)
        shortcut_layout.setSpacing(4)
        for text, handler in (
            ("今天", self.select_today),
            ("近 7 天", self.select_last_seven_days),
            ("本月", self.select_current_month),
            ("上月", self.select_previous_month),
        ):
            button = QPushButton(text)
            button.setObjectName("shortcutButton")
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(handler)
            shortcut_layout.addWidget(button)
        shortcut_layout.addStretch()
        layout.addWidget(shortcut_bar)

        calendars_layout = QHBoxLayout()
        calendars_layout.setSpacing(16)
        self.start_calendar = self._create_calendar(start_date)
        self.end_calendar = self._create_calendar(end_date)
        calendars_layout.addWidget(self._calendar_panel("开始日期", self.start_calendar))
        calendars_layout.addWidget(self._calendar_panel("结束日期", self.end_calendar))
        layout.addLayout(calendars_layout, 1)

        self.start_calendar.selectionChanged.connect(self._sync_end_date)
        self.end_calendar.selectionChanged.connect(self._sync_start_date)

        actions = QHBoxLayout()
        actions.addStretch()
        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("dateRangeCancel")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)
        actions.addWidget(cancel_button)
        confirm_button = QPushButton("确定")
        confirm_button.setObjectName("dateRangeConfirm")
        confirm_button.setCursor(Qt.PointingHandCursor)
        confirm_button.clicked.connect(self.accept)
        actions.addWidget(confirm_button)
        layout.addLayout(actions)

    def _create_calendar(self, selected_date):
        calendar = QCalendarWidget()
        calendar.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        calendar.setFirstDayOfWeek(Qt.Monday)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        calendar.setGridVisible(False)
        calendar.setSelectedDate(selected_date)
        return calendar

    def _calendar_panel(self, title, calendar):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        label = QLabel(title)
        label.setObjectName("calendarTitle")
        layout.addWidget(label)
        layout.addWidget(calendar)
        return panel

    def _sync_end_date(self):
        if self.start_date() > self.end_date():
            self.end_calendar.setSelectedDate(self.start_date())

    def _sync_start_date(self):
        if self.end_date() < self.start_date():
            self.start_calendar.setSelectedDate(self.end_date())

    def _set_range(self, start_date, end_date):
        self.start_calendar.setSelectedDate(start_date)
        self.end_calendar.setSelectedDate(end_date)

    def select_today(self):
        today = QDate.currentDate()
        self._set_range(today, today)

    def select_last_seven_days(self):
        today = QDate.currentDate()
        self._set_range(today.addDays(-6), today)

    def select_current_month(self):
        today = QDate.currentDate()
        first_day = QDate(today.year(), today.month(), 1)
        self._set_range(first_day, first_day.addMonths(1).addDays(-1))

    def select_previous_month(self):
        today = QDate.currentDate()
        first_day = QDate(today.year(), today.month(), 1).addMonths(-1)
        self._set_range(first_day, first_day.addMonths(1).addDays(-1))

    def start_date(self):
        return self.start_calendar.selectedDate()

    def end_date(self):
        return self.end_calendar.selectedDate()


class DateRangePicker(QPushButton):
    def __init__(self, start_date, end_date, parent=None):
        super().__init__(parent)
        self._start_date = start_date
        self._end_date = end_date
        self.setObjectName("dateRangePicker")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.clicked.connect(self.open_picker)
        self._update_text()

    def open_picker(self):
        dialog = DateRangeDialog(self._start_date, self._end_date, self)
        if dialog.exec() == QDialog.Accepted:
            self._start_date = dialog.start_date()
            self._end_date = dialog.end_date()
            self._update_text()

    def start_date(self):
        return self._start_date

    def end_date(self):
        return self._end_date

    def _update_text(self):
        start = self._start_date.toString("yyyy-MM-dd")
        end = self._end_date.toString("yyyy-MM-dd")
        self.setText(f"📅  {start}  至  {end}")
