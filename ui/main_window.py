from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QMessageBox, QGridLayout,
    QScrollArea, QSizePolicy, QButtonGroup, QProgressBar,
    QLineEdit, QAbstractItemView, QMenu, QDialog, QToolTip
)
from PySide6.QtCore import Qt, QDate, QPointF, QTimer
from PySide6.QtGui import QFont, QColor, QIcon, QPainter, QCursor, QPen
from PySide6.QtCharts import (
    QCategoryAxis, QChart, QChartView, QLineSeries, QScatterSeries, QValueAxis
)
from ui.dialogs import TransactionDialog
from ui.account_dialog import AccountFormDialog
from ui.date_range_picker import DateRangePicker
from ui.month_picker import MonthPicker
from ui.confirm_dialog import ConfirmDialog
from datetime import date, datetime


class MainWindow(QMainWindow):
    def __init__(
        self, transaction_service, account_service, auth_service, session
    ):
        super().__init__()
        self.transaction_service = transaction_service
        self.account_service = account_service
        self.auth_service = auth_service
        self.session = session
        self._logged_out = False
        self.setWindowTitle("记账本 - 个人财务管理")
        self.setMinimumSize(1000, 650)
        self.resize(1100, 700)
        self.setup_ui()
        self.nav_buttons[0].setChecked(True)
        self.stacked.setCurrentIndex(0)
        self.refresh_dashboard()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 12, 0)
        content_layout.setSpacing(0)

        header = self.create_header()
        content_layout.addWidget(header)

        self.stacked = QStackedWidget()
        self.pages = [
            self.create_dashboard_page(),
            self.create_transactions_page(),
            self.create_statistics_page(),
        ]
        self.account_page = self.create_account_page()
        for page in self.pages:
            self.stacked.addWidget(page)
        self.stacked.addWidget(self.account_page)
        content_layout.addWidget(self.stacked)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(4)

        logo = QLabel("📒 记账本")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFont(QFont("", 18, QFont.Bold))
        logo.setStyleSheet("color: #1a1a1a; padding: 16px;")
        layout.addWidget(logo)
        layout.addSpacing(16)

        self.nav_buttons = []
        nav_items = [
            ("📊 仪表盘", "dashboard"),
            ("📋 明细", "transactions"),
            ("📈 统计", "statistics"),
        ]
        for idx, (text, _) in enumerate(nav_items):
            btn = QPushButton(text)
            btn.setObjectName("nav_btn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self.on_nav_clicked(i))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        layout.addStretch()
        return sidebar

    def create_header(self):
        header = QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #f0f0f0;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        self.page_title = QLabel("仪表盘")
        self.page_title.setFont(QFont("", 16, QFont.Bold))
        self.page_title.setStyleSheet("color: #1a1a1a;")
        layout.addWidget(self.page_title)

        layout.addStretch()

        self.clock_label = QLabel()
        self.clock_label.setStyleSheet(
            "color: #8c8c8c; font-size: 13px; margin-right: 16px;"
        )
        self.clock_label.setMinimumWidth(166)
        self.clock_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.clock_label)

        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self.update_clock)
        self.update_clock()
        self.clock_timer.start()

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFixedHeight(24)
        separator.setStyleSheet("color: #d9d9d9;")
        layout.addWidget(separator)

        self.account_btn = QPushButton(f"👤 {self.session.username}  ▾")
        self.account_btn.setCursor(Qt.PointingHandCursor)
        self.account_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #1a1a1a;
                font-size: 14px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 6px 16px;
                margin-left: 8px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #1890ff;
                color: #1890ff;
            }
            QPushButton::menu-indicator {
                image: none;
                width: 0;
            }
        """)
        account_menu = QMenu(self.account_btn)
        account_menu.setObjectName("accountMenu")
        account_menu.setStyleSheet("""
            QMenu#accountMenu {
                background-color: #ffffff;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu#accountMenu::item {
                color: #1a1a1a;
                padding: 9px 28px 9px 14px;
                border-radius: 6px;
                font-size: 13px;
            }
            QMenu#accountMenu::item:selected {
                background-color: #e6f7ff;
                color: #1890ff;
            }
            QMenu#accountMenu::separator {
                height: 1px;
                background-color: #f0f0f0;
                margin: 5px 8px;
            }
        """)
        manage_action = account_menu.addAction("账号管理")
        manage_action.triggered.connect(self.on_account_btn_click)
        account_menu.addSeparator()
        logout_action = account_menu.addAction("退出登录")
        logout_action.triggered.connect(self.on_logout)
        self.account_btn.setMenu(account_menu)
        layout.addWidget(self.account_btn)

        return header

    def update_clock(self):
        self.clock_label.setText(datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"))

    def on_account_btn_click(self):
        self.stacked.setCurrentIndex(3)
        self.refresh_accounts()
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.page_title.setText("账号管理")

    def on_logout(self):
        confirmed = ConfirmDialog.ask(
            self,
            "退出登录",
            f"确定要退出账号“{self.session.username}”吗？",
            "退出后需要重新输入账号和密码。",
            "退出登录",
        )
        if confirmed:
            self.auth_service.logout()
            self._logged_out = True
            self.close()

    def on_nav_clicked(self, idx):
        titles = ["仪表盘", "明细", "统计"]
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)
        self.stacked.setCurrentIndex(idx)
        self.page_title.setText(titles[idx])
        if idx == 0:
            self.refresh_dashboard()
        elif idx == 1:
            self.refresh_transactions()
        elif idx == 2:
            self.refresh_statistics()

    # ==================== Dashboard Page ====================
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(14)

        overview_header = QHBoxLayout()
        overview_header.setSpacing(10)
        overview_title = QLabel("财务概览")
        overview_title.setObjectName("dashboard_title")
        overview_header.addWidget(overview_title)
        overview_header.addStretch()
        today = date.today()
        self.dash_period = MonthPicker(today.year, today.month)
        self.dash_period.setFixedSize(178, 38)
        self.dash_period.periodChanged.connect(self.refresh_dashboard)
        overview_header.addWidget(self.dash_period)
        add_button = QPushButton("＋ 记一笔")
        add_button.setObjectName("add_btn")
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.setFixedSize(96, 38)
        add_button.clicked.connect(self.on_add_transaction)
        overview_header.addWidget(add_button)
        layout.addLayout(overview_header)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.income_card = self.create_dashboard_card("收入", "income")
        self.expense_card = self.create_dashboard_card("支出", "expense")
        self.balance_card = self.create_dashboard_card("结余", "balance")
        self.count_card = self.create_dashboard_card("交易笔数", "count")

        cards_layout.addWidget(self.income_card)
        cards_layout.addWidget(self.expense_card)
        cards_layout.addWidget(self.balance_card)
        cards_layout.addWidget(self.count_card)
        layout.addLayout(cards_layout)

        insights_layout = QHBoxLayout()
        insights_layout.setSpacing(12)

        trend_panel = QFrame()
        trend_panel.setObjectName("dashboard_panel")
        trend_layout = QVBoxLayout(trend_panel)
        trend_layout.setContentsMargins(16, 14, 16, 12)
        trend_layout.setSpacing(8)
        trend_title = QLabel("近 6 个月收支趋势")
        trend_title.setObjectName("dashboard_section_title")
        trend_layout.addWidget(trend_title)
        self.dash_chart = QChart()
        self.dash_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.dash_chart.setBackgroundVisible(False)
        self.dash_chart.legend().setAlignment(Qt.AlignBottom)
        self.dash_chart.legend().setLabelColor(QColor("#595959"))
        self.dash_chart_view = QChartView(self.dash_chart)
        self.dash_chart_view.setRenderHint(QPainter.Antialiasing)
        self.dash_chart_view.setMinimumHeight(160)
        self.dash_chart_view.setMaximumHeight(210)
        trend_layout.addWidget(self.dash_chart_view)
        insights_layout.addWidget(trend_panel, 3)

        category_panel = QFrame()
        category_panel.setObjectName("dashboard_panel")
        category_layout = QVBoxLayout(category_panel)
        category_layout.setContentsMargins(16, 14, 16, 12)
        category_layout.setSpacing(8)
        category_title = QLabel("本月支出构成")
        category_title.setObjectName("dashboard_section_title")
        category_layout.addWidget(category_title)
        self.dash_category_layout = QVBoxLayout()
        self.dash_category_layout.setSpacing(8)
        category_layout.addLayout(self.dash_category_layout)
        category_layout.addStretch()
        insights_layout.addWidget(category_panel, 2)
        layout.addLayout(insights_layout)

        recent_header = QHBoxLayout()
        recent_title = QLabel("最近交易")
        recent_title.setObjectName("dashboard_section_title")
        recent_header.addWidget(recent_title)
        recent_header.addStretch()
        view_all_button = QPushButton("查看全部  →")
        view_all_button.setObjectName("link_btn")
        view_all_button.setCursor(Qt.PointingHandCursor)
        view_all_button.clicked.connect(lambda: self.on_nav_clicked(1))
        recent_header.addWidget(view_all_button)
        layout.addLayout(recent_header)

        self.dash_table = QTableWidget()
        self.dash_table.setColumnCount(5)
        self.dash_table.setHorizontalHeaderLabels(["日期", "类型", "分类", "金额", "备注"])
        self.dash_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dash_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.dash_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dash_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dash_table.verticalHeader().setVisible(False)
        self.dash_table.setAlternatingRowColors(True)
        self.dash_table.setMaximumHeight(190)
        layout.addWidget(self.dash_table)

        return page

    def create_dashboard_card(self, title, kind):
        card = QFrame()
        card.setObjectName(f"dashboard_card_{kind}")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("dashboard_card_title")
        card_layout.addWidget(title_label)

        value_label = QLabel("0")
        value_label.setObjectName(f"dashboard_value_{kind}")
        card_layout.addWidget(value_label)

        detail_label = QLabel("")
        detail_label.setObjectName("dashboard_card_detail")
        card_layout.addWidget(detail_label)

        card._value_label = value_label
        card._detail_label = detail_label
        return card

    def create_stat_card(self, title, value, kind):
        card = QFrame()
        card.setObjectName(f"stat_card_{kind}")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("stat_title")
        card_layout.addWidget(title_label)

        value_label = QLabel(f"¥ {value}")
        value_label.setObjectName(f"stat_value_{kind}")
        card_layout.addWidget(value_label)

        card._value_label = value_label
        card._title_label = title_label
        return card

    def refresh_dashboard(self, *args):
        year = self.dash_period.year()
        month = self.dash_period.month()
        selected_month = QDate(year, month, 1)
        next_month = selected_month.addMonths(1)
        previous_month = selected_month.addMonths(-1)
        start = selected_month.toString("yyyy-MM-dd")
        end = next_month.toString("yyyy-MM-dd")

        summary = self.transaction_service.get_summary(start, end)
        previous = self.transaction_service.get_monthly_summary(
            previous_month.year(), previous_month.month()
        )
        transactions = self.transaction_service.get_transactions(
            start_date=start, end_date=next_month.addDays(-1).toString("yyyy-MM-dd")
        )

        self.income_card._value_label.setText(f"¥ {summary['total_income']:,.2f}")
        self.expense_card._value_label.setText(f"¥ {summary['total_expense']:,.2f}")
        self.balance_card._value_label.setText(f"¥ {summary['balance']:,.2f}")
        self.count_card._value_label.setText(f"{len(transactions)} 笔")
        self.income_card._detail_label.setText(
            self._comparison_text(summary['total_income'], previous['total_income'])
        )
        self.expense_card._detail_label.setText(
            self._comparison_text(summary['total_expense'], previous['total_expense'])
        )
        income = summary['total_income']
        balance_rate = summary['balance'] / income * 100 if income else 0
        self.balance_card._detail_label.setText(f"结余率 {balance_rate:.1f}%")
        days = max(1, next_month.addDays(-1).day())
        self.count_card._detail_label.setText(f"日均 {len(transactions) / days:.1f} 笔")

        self._refresh_dashboard_chart(selected_month)
        self._refresh_dashboard_categories(start, end)

        recent = self.transaction_service.get_transactions()[:5]
        self.dash_table.setRowCount(len(recent))
        for row, t in enumerate(recent):
            self._fill_table_row(self.dash_table, row, t)

    def _comparison_text(self, current, previous):
        if previous == 0:
            return "较上月 --" if current == 0 else "较上月 新增"
        change = (current - previous) / previous * 100
        arrow = "↑" if change >= 0 else "↓"
        return f"较上月 {arrow} {abs(change):.1f}%"

    def _refresh_dashboard_chart(self, selected_month):
        labels = []
        income_values = []
        expense_values = []
        maximum = 0
        for offset in range(-5, 1):
            month_date = selected_month.addMonths(offset)
            summary = self.transaction_service.get_monthly_summary(
                month_date.year(), month_date.month()
            )
            income_values.append(summary['total_income'])
            expense_values.append(summary['total_expense'])
            maximum = max(
                maximum, summary['total_income'], summary['total_expense']
            )
            labels.append(f"{month_date.month()}月")

        if maximum >= 10000:
            divisor, suffix = 10000, "万"
        elif maximum >= 1000:
            divisor, suffix = 1000, "k"
        else:
            divisor, suffix = 1, ""

        self.dash_chart.removeAllSeries()
        for axis in self.dash_chart.axes():
            self.dash_chart.removeAxis(axis)

        income_line = QLineSeries()
        expense_line = QLineSeries()
        income_line.setName("收入")
        expense_line.setName("支出")
        income_line.setColor(QColor("#52c41a"))
        expense_line.setColor(QColor("#f5222d"))
        income_line.setPen(QPen(QColor("#52c41a"), 2.5))
        expense_line.setPen(QPen(QColor("#f5222d"), 2.5))
        income_line.setPointsVisible(True)
        expense_line.setPointsVisible(True)
        income_line.setMarkerSize(7)
        expense_line.setMarkerSize(7)

        for index, (income, expense) in enumerate(zip(income_values, expense_values)):
            income_point = QPointF(index, income / divisor)
            expense_point = QPointF(index, expense / divisor)
            income_line.append(income_point)
            expense_line.append(expense_point)

        income_current = QScatterSeries()
        expense_current = QScatterSeries()
        income_current.append(5, income_values[-1] / divisor)
        expense_current.append(5, expense_values[-1] / divisor)
        income_current.setColor(QColor("#52c41a"))
        expense_current.setColor(QColor("#f5222d"))
        income_current.setBorderColor(QColor("#ffffff"))
        expense_current.setBorderColor(QColor("#ffffff"))
        income_current.setMarkerSize(12)
        expense_current.setMarkerSize(12)

        chart_series = (income_line, expense_line, income_current, expense_current)
        for series in chart_series:
            self.dash_chart.addSeries(series)

        category_axis = QCategoryAxis()
        for index, label in enumerate(labels):
            category_axis.append(label, index)
        category_axis.setRange(0, 5)
        category_axis.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        value_axis = QValueAxis()
        value_axis.setLabelFormat(f"%.1f{suffix}" if suffix else "%.0f")
        scaled_maximum = maximum / divisor
        value_axis.setRange(0, scaled_maximum * 1.15 if maximum else 100)
        value_axis.setTickCount(5)
        self.dash_chart.addAxis(category_axis, Qt.AlignBottom)
        self.dash_chart.addAxis(value_axis, Qt.AlignLeft)
        for series in chart_series:
            series.attachAxis(category_axis)
            series.attachAxis(value_axis)

        for series in (income_current, expense_current):
            for marker in self.dash_chart.legend().markers(series):
                marker.setVisible(False)

        income_line.hovered.connect(
            lambda point, state: self._show_chart_tooltip("收入", point, state, divisor)
        )
        expense_line.hovered.connect(
            lambda point, state: self._show_chart_tooltip("支出", point, state, divisor)
        )

    def _show_chart_tooltip(self, name, point, state, divisor):
        if state:
            QToolTip.showText(
                QCursor.pos(), f"{name}：¥ {point.y() * divisor:,.2f}", self.dash_chart_view
            )
        else:
            QToolTip.hideText()

    def _refresh_dashboard_categories(self, start, end):
        while self.dash_category_layout.count():
            item = self.dash_category_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        categories = self.transaction_service.get_category_summary(
            start, end, 'expense'
        )[:4]
        total = sum(item['total'] for item in categories)
        if not categories:
            empty = QLabel("本月暂无支出")
            empty.setObjectName("dashboard_empty")
            empty.setAlignment(Qt.AlignCenter)
            self.dash_category_layout.addWidget(empty)
            return

        for category in categories:
            row = QWidget()
            row_layout = QVBoxLayout(row)
            row_layout.setContentsMargins(0, 2, 0, 2)
            row_layout.setSpacing(4)
            info_layout = QHBoxLayout()
            name = QLabel(f"{category['icon']} {category['name']}")
            name.setObjectName("dashboard_category_name")
            info_layout.addWidget(name)
            info_layout.addStretch()
            amount = QLabel(f"¥ {category['total']:,.2f}")
            amount.setObjectName("dashboard_category_amount")
            info_layout.addWidget(amount)
            row_layout.addLayout(info_layout)
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(int(category['total'] / total * 100) if total else 0)
            progress.setTextVisible(False)
            progress.setObjectName("dashboard_category_progress")
            row_layout.addWidget(progress)
            self.dash_category_layout.addWidget(row)

    def _fill_table_row(self, table, row, t):
        date_item = QTableWidgetItem(t['date'])
        date_item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, 0, date_item)

        type_text = "收入" if t['type'] == 'income' else "支出"
        type_item = QTableWidgetItem(type_text)
        type_item.setTextAlignment(Qt.AlignCenter)
        if t['type'] == 'income':
            type_item.setForeground(QColor("#52c41a"))
        else:
            type_item.setForeground(QColor("#f5222d"))
        table.setItem(row, 1, type_item)

        cat_text = f"{t.get('category_icon', '')} {t.get('category_name', '')}"
        cat_item = QTableWidgetItem(cat_text)
        cat_item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, 2, cat_item)

        amount_text = f"¥ {t['amount']:,.2f}"
        amount_item = QTableWidgetItem(amount_text)
        amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if t['type'] == 'income':
            amount_item.setForeground(QColor("#52c41a"))
        else:
            amount_item.setForeground(QColor("#f5222d"))
        amount_item.setFont(QFont("", 11, QFont.Bold))
        table.setItem(row, 3, amount_item)

        note_item = QTableWidgetItem(t.get('note', ''))
        table.setItem(row, 4, note_item)

    # ==================== Transactions Page ====================
    def create_transactions_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(12)

        filter_bar = QFrame()
        filter_bar.setObjectName("filterBar")
        filter_layout = QHBoxLayout(filter_bar)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(8)

        date_label = QLabel("日期")
        date_label.setObjectName("filter_label")
        filter_layout.addWidget(date_label)
        self.tx_date_range = DateRangePicker(
            QDate.currentDate().addMonths(-1), QDate.currentDate()
        )
        self.tx_date_range.setMinimumWidth(235)
        self.tx_date_range.setFixedHeight(38)
        filter_layout.addWidget(self.tx_date_range, 4)

        type_label = QLabel("类型")
        type_label.setObjectName("filter_label")
        self.tx_type_filter = QComboBox()
        self.tx_type_filter.setObjectName("txTypeFilter")
        self.tx_type_filter.addItems(["全部", "收入", "支出"])
        self.tx_type_filter.setItemData(0, QColor("#595959"), Qt.ForegroundRole)
        self.tx_type_filter.setItemData(1, QColor("#389e0d"), Qt.ForegroundRole)
        self.tx_type_filter.setItemData(2, QColor("#cf1322"), Qt.ForegroundRole)
        self.tx_type_filter.setMinimumWidth(92)
        self.tx_type_filter.setMaximumWidth(118)
        self.tx_type_filter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.tx_type_filter.setFixedHeight(38)
        self.tx_type_filter.currentIndexChanged.connect(
            self.update_type_filter_style
        )
        self.update_type_filter_style(0)
        filter_layout.addWidget(type_label)
        filter_layout.addWidget(self.tx_type_filter, 1)

        cat_label = QLabel("分类")
        cat_label.setObjectName("filter_label")
        self.tx_cat_filter = QComboBox()
        self.tx_cat_filter.addItem("全部", None)
        for cat in self.transaction_service.get_categories():
            self.tx_cat_filter.addItem(f"{cat['icon']} {cat['name']}", cat['id'])
        self.tx_cat_filter.setMinimumWidth(80)
        self.tx_cat_filter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.tx_cat_filter.setFixedHeight(38)
        filter_layout.addWidget(cat_label)
        filter_layout.addWidget(self.tx_cat_filter, 2)

        query_btn = QPushButton("🔍 查询")
        query_btn.setObjectName("query_btn")
        query_btn.setCursor(Qt.PointingHandCursor)
        query_btn.setMinimumWidth(72)
        query_btn.setFixedHeight(38)
        query_btn.clicked.connect(self.refresh_transactions)
        filter_layout.addWidget(query_btn)

        add_btn = QPushButton("＋ 记一笔")
        add_btn.setObjectName("add_btn")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setMinimumWidth(88)
        add_btn.setFixedHeight(38)
        add_btn.clicked.connect(self.on_add_transaction)
        filter_layout.addWidget(add_btn)

        layout.addWidget(filter_bar)

        self.tx_summary_label = QLabel("")
        self.tx_summary_label.setObjectName("filter_label")
        layout.addWidget(self.tx_summary_label)

        self.tx_table = QTableWidget()
        self.tx_table.setColumnCount(7)
        self.tx_table.setHorizontalHeaderLabels(["日期", "类型", "分类", "金额", "备注", "操作", ""])
        self.tx_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tx_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.tx_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.tx_table.setColumnWidth(5, 70)
        self.tx_table.setColumnWidth(6, 70)
        self.tx_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tx_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tx_table.verticalHeader().setVisible(False)
        self.tx_table.setAlternatingRowColors(True)
        layout.addWidget(self.tx_table)

        return page

    def update_type_filter_style(self, index):
        filter_types = ("all", "income", "expense")
        self.tx_type_filter.setProperty("filterType", filter_types[index])
        self.tx_type_filter.style().unpolish(self.tx_type_filter)
        self.tx_type_filter.style().polish(self.tx_type_filter)

    def refresh_transactions(self):
        start = self.tx_date_range.start_date().toString("yyyy-MM-dd")
        end = self.tx_date_range.end_date().toString("yyyy-MM-dd")
        type_idx = self.tx_type_filter.currentIndex()
        type_map = {0: None, 1: 'income', 2: 'expense'}
        tx_type = type_map[type_idx]
        cat_id = self.tx_cat_filter.currentData()

        transactions = self.transaction_service.get_transactions(
            start_date=start, end_date=end,
            type=tx_type, category_id=cat_id
        )

        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        self.tx_summary_label.setText(
            f"共 {len(transactions)} 笔  |  "
            f"收入: <span style='color:#52c41a;font-weight:bold'>¥ {total_income:,.2f}</span>  |  "
            f"支出: <span style='color:#f5222d;font-weight:bold'>¥ {total_expense:,.2f}</span>  |  "
            f"结余: <span style='color:#1890ff;font-weight:bold'>¥ {total_income - total_expense:,.2f}</span>"
        )

        self.tx_table.setRowCount(len(transactions))
        for row, t in enumerate(transactions):
            self._fill_txn_row(row, t)

    def _fill_txn_row(self, row, t):
        date_item = QTableWidgetItem(t['date'])
        date_item.setTextAlignment(Qt.AlignCenter)
        self.tx_table.setItem(row, 0, date_item)

        type_text = "收入" if t['type'] == 'income' else "支出"
        type_item = QTableWidgetItem(type_text)
        type_item.setTextAlignment(Qt.AlignCenter)
        type_item.setForeground(QColor("#52c41a" if t['type'] == 'income' else "#f5222d"))
        self.tx_table.setItem(row, 1, type_item)

        cat_text = f"{t.get('category_icon', '')} {t.get('category_name', '')}"
        cat_item = QTableWidgetItem(cat_text)
        cat_item.setTextAlignment(Qt.AlignCenter)
        self.tx_table.setItem(row, 2, cat_item)

        amount_text = f"¥ {t['amount']:,.2f}"
        amount_item = QTableWidgetItem(amount_text)
        amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        amount_item.setForeground(QColor("#52c41a" if t['type'] == 'income' else "#f5222d"))
        amount_item.setFont(QFont("", 11, QFont.Bold))
        self.tx_table.setItem(row, 3, amount_item)

        note_item = QTableWidgetItem(t.get('note', ''))
        self.tx_table.setItem(row, 4, note_item)

        edit_btn = QPushButton("✏️ 编辑")
        edit_btn.setObjectName("edit_btn")
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.clicked.connect(lambda checked, t=t: self.on_edit_transaction(t))
        self.tx_table.setCellWidget(row, 5, edit_btn)

        del_btn = QPushButton("🗑 删除")
        del_btn.setObjectName("delete_btn")
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.clicked.connect(lambda checked, item=t: self.on_delete_transaction(item))
        self.tx_table.setCellWidget(row, 6, del_btn)

    def on_add_transaction(self):
        dialog = TransactionDialog(self.transaction_service, parent=self)
        if dialog.exec() == TransactionDialog.Accepted:
            data = dialog.get_data()
            try:
                self.transaction_service.add_transaction(**data)
            except Exception as error:
                QMessageBox.critical(self, "新增失败", f"记录保存失败：{error}")
                return
            transaction_date = QDate.fromString(data['date'], "yyyy-MM-dd")
            self.tx_date_range.include_date(transaction_date)
            self.refresh_transactions()
            self.refresh_dashboard()

    def on_edit_transaction(self, t):
        dialog = TransactionDialog(
            self.transaction_service, transaction=t, parent=self
        )
        if dialog.exec() == TransactionDialog.Accepted:
            data = dialog.get_data()
            self.transaction_service.update_transaction(t['id'], **data)
            self.refresh_transactions()
            self.refresh_dashboard()

    def on_delete_transaction(self, transaction):
        transaction_type = "收入" if transaction['type'] == 'income' else "支出"
        confirmed = ConfirmDialog.ask(
            self,
            "删除明细",
            f"确定删除这笔{transaction_type} ¥ {transaction['amount']:,.2f} 吗？",
            f"记录日期：{transaction['date']}。删除后无法恢复。",
            "确认删除",
        )
        if confirmed:
            self.transaction_service.delete_transaction(transaction['id'])
            self.refresh_transactions()
            self.refresh_dashboard()

    # ==================== Statistics Page ====================
    def create_statistics_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(12)

        filter_bar = QFrame()
        filter_bar.setObjectName("filterBar")
        header = QHBoxLayout(filter_bar)
        header.setContentsMargins(16, 12, 16, 12)
        header.setSpacing(8)

        period_label = QLabel("统计周期")
        period_label.setObjectName("filter_label")
        header.addWidget(period_label)

        today = date.today()
        self.stat_period = MonthPicker(today.year, today.month)
        self.stat_period.setMinimumWidth(170)
        self.stat_period.setMaximumWidth(230)
        self.stat_period.setFixedHeight(38)
        header.addWidget(self.stat_period, 2)

        query_btn = QPushButton("🔍 查询")
        query_btn.setObjectName("query_btn")
        query_btn.setCursor(Qt.PointingHandCursor)
        query_btn.setMinimumWidth(72)
        query_btn.setFixedHeight(38)
        query_btn.clicked.connect(self.refresh_statistics)
        header.addWidget(query_btn)

        header.addStretch()
        layout.addWidget(filter_bar)

        stat_cards = QHBoxLayout()
        stat_cards.setSpacing(16)
        self.stat_income_card = self.create_stat_card("总收入", "0.00", "income")
        self.stat_expense_card = self.create_stat_card("总支出", "0.00", "expense")
        self.stat_balance_card = self.create_stat_card("结余", "0.00", "balance")
        stat_cards.addWidget(self.stat_income_card)
        stat_cards.addWidget(self.stat_expense_card)
        stat_cards.addWidget(self.stat_balance_card)
        layout.addLayout(stat_cards)

        layout.addSpacing(8)

        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(8)
        self.stat_type_group = QButtonGroup(self)
        self.stat_tab_expense = QPushButton("📤 支出分类")
        self.stat_tab_income = QPushButton("📥 收入分类")
        for btn in [self.stat_tab_expense, self.stat_tab_income]:
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #595959;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #1890ff;
                    color: white;
                }
            """)
            tabs_layout.addWidget(btn)
        self.stat_type_group.addButton(self.stat_tab_expense)
        self.stat_type_group.addButton(self.stat_tab_income)
        self.stat_tab_expense.setChecked(True)
        self.stat_tab_expense.clicked.connect(self.refresh_statistics)
        self.stat_tab_income.clicked.connect(self.refresh_statistics)
        tabs_layout.addStretch()
        layout.addLayout(tabs_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.stat_content = QWidget()
        self.stat_content_layout = QVBoxLayout(self.stat_content)
        self.stat_content_layout.setContentsMargins(0, 0, 0, 0)
        self.stat_content_layout.setSpacing(8)
        scroll.setWidget(self.stat_content)
        layout.addWidget(scroll)

        return page

    def refresh_statistics(self):
        year = self.stat_period.year()
        month = self.stat_period.month()

        start = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end = f"{year+1:04d}-01-01"
        else:
            end = f"{year:04d}-{month+1:02d}-01"

        summary = self.transaction_service.get_summary(start, end)
        self.stat_income_card._value_label.setText(f"¥ {summary['total_income']:,.2f}")
        self.stat_expense_card._value_label.setText(f"¥ {summary['total_expense']:,.2f}")
        self.stat_balance_card._value_label.setText(f"¥ {summary['balance']:,.2f}")

        tx_type = 'income' if self.stat_tab_income.isChecked() else 'expense'
        categories = self.transaction_service.get_category_summary(
            start, end, tx_type
        )

        while self.stat_content_layout.count():
            item = self.stat_content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        total = sum(c['total'] for c in categories) if categories else 0

        if not categories:
            empty = QLabel("暂无数据")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #8c8c8c; font-size: 14px; padding: 40px;")
            self.stat_content_layout.addWidget(empty)
            self.stat_content_layout.addStretch()
            return

        for cat in categories:
            pct = (cat['total'] / total * 100) if total > 0 else 0
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background-color: #fafafa;
                    border-radius: 10px;
                    padding: 8px;
                }
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(16, 12, 16, 12)

            icon_label = QLabel(cat.get('icon') or '📁')
            icon_label.setFont(QFont("", 18))
            row_layout.addWidget(icon_label)

            name_layout = QVBoxLayout()
            name_label = QLabel(cat.get('name') or '未分类')
            name_label.setFont(QFont("", 13, QFont.Bold))
            name_label.setStyleSheet("color: #1a1a1a;")
            name_layout.addWidget(name_label)

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(pct))
            bar.setFormat(f"{pct:.1f}%")
            bar_color = "#52c41a" if tx_type == 'income' else "#f5222d"
            bar.setStyleSheet(f"""
                QProgressBar {{ border: none; border-radius: 6px; background-color: #f0f0f0;
                    text-align: center; min-height: 16px; max-height: 16px;
                    color: #595959; font-size: 11px; }}
                QProgressBar::chunk {{ border-radius: 6px; background-color: {bar_color}; }}
            """)
            name_layout.addWidget(bar)
            row_layout.addLayout(name_layout, 1)

            amount_label = QLabel(f"¥ {cat['total']:,.2f}")
            amount_label.setFont(QFont("", 14, QFont.Bold))
            if tx_type == 'income':
                amount_label.setStyleSheet("color: #52c41a;")
            else:
                amount_label.setStyleSheet("color: #f5222d;")
            row_layout.addWidget(amount_label)

            self.stat_content_layout.addWidget(row)

        self.stat_content_layout.addStretch()

    # ==================== Account Management Page ====================
    def create_account_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("账号列表")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title.setStyleSheet("color: #1a1a1a; padding: 8px 0;")
        header.addWidget(title)
        header.addStretch()

        add_btn = QPushButton("＋  新增账号")
        add_btn.setObjectName("account_add_btn")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setFixedSize(126, 40)
        add_btn.clicked.connect(self.on_add_account)
        header.addWidget(add_btn)

        layout.addLayout(header)

        self.account_table = QTableWidget()
        self.account_table.setColumnCount(5)
        self.account_table.setHorizontalHeaderLabels(
            ["账号编号", "用户名", "创建时间", "更新时间", "操作"]
        )
        self.account_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.account_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.account_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.account_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.account_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.account_table.setColumnWidth(4, 140)
        self.account_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.account_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.account_table.setAlternatingRowColors(True)
        self.account_table.verticalHeader().setVisible(False)
        self.account_table.setShowGrid(False)
        layout.addWidget(self.account_table)

        return page

    def refresh_accounts(self):
        accounts = self.account_service.get_accounts()
        self.account_table.setRowCount(len(accounts))
        self.account_table.verticalHeader().setDefaultSectionSize(72)

        for row, acc in enumerate(accounts):
            accountcode_item = QTableWidgetItem(str(acc['accountcode']))
            accountcode_item.setTextAlignment(Qt.AlignCenter)
            accountcode_item.setForeground(QColor("#1890ff"))
            self.account_table.setItem(row, 0, accountcode_item)

            username_item = QTableWidgetItem(acc['username'])
            username_item.setFont(QFont("Microsoft YaHei", 11))
            username_item.setTextAlignment(Qt.AlignCenter)
            self.account_table.setItem(row, 1, username_item)

            create_time_item = QTableWidgetItem(acc.get('createTime', ''))
            create_time_item.setTextAlignment(Qt.AlignCenter)
            create_time_item.setForeground(QColor("#8c8c8c"))
            create_time_item.setFont(QFont("Microsoft YaHei", 9))
            self.account_table.setItem(row, 2, create_time_item)

            update_time_item = QTableWidgetItem(acc.get('updateTime', ''))
            update_time_item.setTextAlignment(Qt.AlignCenter)
            update_time_item.setForeground(QColor("#8c8c8c"))
            update_time_item.setFont(QFont("Microsoft YaHei", 9))
            self.account_table.setItem(row, 3, update_time_item)

            action_widget = QWidget()
            action_widget.setStyleSheet("background-color: transparent;")
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(8, 4, 8, 4)
            action_layout.setSpacing(8)

            edit_btn = QPushButton("编辑")
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setFixedSize(56, 28)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #1890ff;
                    border: 1px solid #1890ff;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1890ff;
                    color: white;
                }
            """)
            edit_btn.clicked.connect(lambda checked, a=acc: self.on_edit_account(a))
            action_layout.addWidget(edit_btn)
            action_layout.addStretch()

            is_admin = acc['username'] == 'admin'
            del_btn = QPushButton("删除")
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setFixedSize(56, 28)
            del_color = "#bfbfbf" if is_admin else "#ff4d4f"
            del_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {del_color};
                    border: 1px solid {del_color};
                    border-radius: 4px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {del_color};
                    color: white;
                }}
            """)
            del_btn.setEnabled(not is_admin)
            del_btn.clicked.connect(lambda checked, account=acc: self.on_delete_account(account))
            action_layout.addWidget(del_btn)

            self.account_table.setCellWidget(row, 4, action_widget)

    def on_add_account(self):
        dialog = AccountFormDialog(self.account_service, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.refresh_accounts()

    def on_edit_account(self, account):
        dialog = AccountFormDialog(
            self.account_service, account=account, parent=self
        )
        if dialog.exec() == QDialog.Accepted:
            self.refresh_accounts()

    def on_delete_account(self, account):
        confirmed = ConfirmDialog.ask(
            self,
            "删除账号",
            f"确定删除账号“{account['username']}”吗？",
            "删除后该账号将无法登录，此操作无法恢复。",
            "确认删除",
        )
        if confirmed:
            success, message = self.account_service.delete_account(account['id'])
            if success:
                self.refresh_accounts()
            else:
                QMessageBox.critical(self, "错误", message)
