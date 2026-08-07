from PySide6.QtCore import QDate, QEvent, QLocale, QObject, Qt
from PySide6.QtWidgets import (
    QCalendarWidget, QDialog, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpinBox, QToolButton, QVBoxLayout, QWidget
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
    min-width: 28px;
    min-height: 28px;
}

QCalendarWidget QToolButton:hover {
    background-color: #e6f7ff;
    color: #1890ff;
}

QCalendarWidget QToolButton#qt_calendar_prevmonth,
QCalendarWidget QToolButton#qt_calendar_nextmonth {
    color: #1890ff;
    background-color: #ffffff;
    border: 1px solid #d9e8f5;
    font-size: 20px;
    font-weight: bold;
    padding: 0;
}

QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
    background-color: #e6f7ff;
    border-color: #40a9ff;
}

QCalendarWidget QSpinBox#qt_calendar_yearedit {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #91d5ff;
    border-radius: 5px;
    padding: 4px 28px 4px 8px;
    min-width: 82px;
    min-height: 26px;
    font-size: 14px;
    font-weight: bold;
}

QCalendarWidget QToolButton#yearIncreaseButton,
QCalendarWidget QToolButton#yearDecreaseButton {
    background-color: #e6f7ff;
    color: #096dd9;
    border: none;
    border-left: 1px solid #91d5ff;
    border-radius: 0;
    padding: 0;
    min-width: 22px;
    min-height: 0;
    font-size: 14px;
    font-weight: bold;
}

QCalendarWidget QToolButton#yearIncreaseButton:hover,
QCalendarWidget QToolButton#yearDecreaseButton:hover {
    background-color: #bae7ff;
    color: #0050b3;
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


class YearStepButtons(QObject):
    def __init__(self, year_edit):
        super().__init__(year_edit)
        self.year_edit = year_edit
        self.increase_button = self._create_button("+", "yearIncreaseButton")
        self.decrease_button = self._create_button("-", "yearDecreaseButton")
        self.increase_button.clicked.connect(self.year_edit.stepUp)
        self.decrease_button.clicked.connect(self.year_edit.stepDown)
        self.year_edit.setButtonSymbols(QSpinBox.NoButtons)
        self.year_edit.installEventFilter(self)
        self._update_geometry()

    def _create_button(self, text, object_name):
        button = QToolButton(self.year_edit)
        button.setObjectName(object_name)
        button.setText(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setAutoRepeat(True)
        button.setFocusPolicy(Qt.NoFocus)
        button.show()
        return button

    def eventFilter(self, watched, event):
        if watched is self.year_edit and event.type() in (QEvent.Resize, QEvent.Show):
            self._update_geometry()
        return super().eventFilter(watched, event)

    def _update_geometry(self):
        button_width = 22
        half_height = max(1, self.year_edit.height() // 2)
        x = self.year_edit.width() - button_width - 1
        self.increase_button.setGeometry(x, 1, button_width, half_height)
        self.decrease_button.setGeometry(
            x, half_height, button_width, self.year_edit.height() - half_height - 1
        )
        self.increase_button.raise_()
        self.decrease_button.raise_()


def create_calendar(selected_date):
    calendar = QCalendarWidget()
    calendar.setLocale(QLocale(QLocale.Chinese, QLocale.China))
    calendar.setFirstDayOfWeek(Qt.Monday)
    calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
    calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
    calendar.setGridVisible(False)
    calendar.setSelectedDate(selected_date)

    previous_button = calendar.findChild(QToolButton, "qt_calendar_prevmonth")
    next_button = calendar.findChild(QToolButton, "qt_calendar_nextmonth")
    if previous_button:
        previous_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
        previous_button.setText("<")
    if next_button:
        next_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
        next_button.setText(">")

    year_edit = calendar.findChild(QSpinBox, "qt_calendar_yearedit")
    if year_edit:
        year_edit.setAlignment(Qt.AlignCenter)
        year_edit._step_buttons = YearStepButtons(year_edit)
    return calendar


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
        self.start_calendar = create_calendar(start_date)
        self.end_calendar = create_calendar(end_date)
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


class DatePickerDialog(QDialog):
    def __init__(self, selected_date, parent=None):
        super().__init__(parent)
        self.setObjectName("dateRangeDialog")
        self.setWindowTitle("选择日期")
        self.setFixedSize(380, 400)
        self.setStyleSheet(DATE_RANGE_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        title_row = QHBoxLayout()
        title = QLabel("选择日期")
        title.setObjectName("dateRangeTitle")
        title_row.addWidget(title)
        title_row.addStretch()
        today_button = QPushButton("今天")
        today_button.setObjectName("shortcutButton")
        today_button.setCursor(Qt.PointingHandCursor)
        today_button.clicked.connect(self.select_today)
        title_row.addWidget(today_button)
        layout.addLayout(title_row)

        self.calendar = create_calendar(selected_date)
        layout.addWidget(self.calendar, 1)

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

    def select_today(self):
        self.calendar.setSelectedDate(QDate.currentDate())

    def selected_date(self):
        return self.calendar.selectedDate()


class DatePicker(QPushButton):
    def __init__(self, selected_date=None, parent=None):
        super().__init__(parent)
        self._date = selected_date or QDate.currentDate()
        self.setObjectName("dateRangePicker")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.clicked.connect(self.open_picker)
        self._update_text()

    def open_picker(self):
        dialog = DatePickerDialog(self._date, self)
        if dialog.exec() == QDialog.Accepted:
            self.setDate(dialog.selected_date())

    def setDate(self, selected_date):
        if selected_date.isValid():
            self._date = selected_date
            self._update_text()

    def date(self):
        return self._date

    def _update_text(self):
        self.setText(f"📅  {self._date.toString('yyyy-MM-dd')}")
