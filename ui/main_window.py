from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDateEdit, QMessageBox, QGridLayout,
    QScrollArea, QSizePolicy, QButtonGroup, QProgressBar,
    QLineEdit, QAbstractItemView
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor, QIcon
from database import Database
from ui.dialogs import TransactionDialog
from datetime import date, datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
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
        for page in self.pages:
            self.stacked.addWidget(page)
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

        today_label = QLabel(date.today().strftime("%Y年%m月%d日"))
        today_label.setStyleSheet("color: #8c8c8c; font-size: 13px;")
        layout.addWidget(today_label)

        return header

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
        layout.setSpacing(16)

        year = date.today().year
        month = date.today().month
        self.dash_year_label = QLabel(f"{year} 年")
        self.dash_month_label = QLabel(f"{month} 月")

        month_sel = QHBoxLayout()
        month_sel.addWidget(QLabel("💰 本月概览  "))
        month_sel.addStretch()
        month_sel.addWidget(self.dash_year_label)
        month_sel.addWidget(QLabel(" · "))
        month_sel.addWidget(self.dash_month_label)
        layout.addLayout(month_sel)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.income_card = self.create_stat_card("本月收入", "0.00", "income")
        self.expense_card = self.create_stat_card("本月支出", "0.00", "expense")
        self.balance_card = self.create_stat_card("本月结余", "0.00", "balance")
        self.count_card = self.create_stat_card("交易笔数", "0", "income")

        cards_layout.addWidget(self.income_card)
        cards_layout.addWidget(self.expense_card)
        cards_layout.addWidget(self.balance_card)
        cards_layout.addWidget(self.count_card)
        layout.addLayout(cards_layout)

        layout.addSpacing(8)
        recent_title = QLabel("📋 最近交易")
        recent_title.setFont(QFont("", 15, QFont.Bold))
        recent_title.setStyleSheet("color: #1a1a1a; padding-top: 8px;")
        layout.addWidget(recent_title)

        self.dash_table = QTableWidget()
        self.dash_table.setColumnCount(5)
        self.dash_table.setHorizontalHeaderLabels(["日期", "类型", "分类", "金额", "备注"])
        self.dash_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dash_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.dash_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dash_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dash_table.verticalHeader().setVisible(False)
        self.dash_table.setAlternatingRowColors(True)
        layout.addWidget(self.dash_table)

        return page

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

    def refresh_dashboard(self):
        today = date.today()
        start = f"{today.year:04d}-{today.month:02d}-01"
        if today.month == 12:
            end = f"{today.year+1:04d}-01-01"
        else:
            end = f"{today.year:04d}-{today.month+1:02d}-01"

        summary = self.db.get_summary(start, end)
        transactions = self.db.get_transactions(start_date=start, end_date=end)

        self.income_card._value_label.setText(f"¥ {summary['total_income']:,.2f}")
        self.expense_card._value_label.setText(f"¥ {summary['total_expense']:,.2f}")
        self.balance_card._value_label.setText(f"¥ {summary['balance']:,.2f}")
        self.count_card._value_label.setText(f"{len(transactions)}")

        recent = self.db.get_transactions()[:10]
        self.dash_table.setRowCount(len(recent))
        for row, t in enumerate(recent):
            self._fill_table_row(self.dash_table, row, t)

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

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)

        filter_layout.addWidget(QLabel("从"))
        self.tx_start_date = QDateEdit()
        self.tx_start_date.setCalendarPopup(True)
        self.tx_start_date.setDisplayFormat("yyyy-MM-dd")
        self.tx_start_date.setDate(QDate.currentDate().addMonths(-1))
        self.tx_start_date.setFixedWidth(140)
        filter_layout.addWidget(self.tx_start_date)

        filter_layout.addWidget(QLabel("到"))
        self.tx_end_date = QDateEdit()
        self.tx_end_date.setCalendarPopup(True)
        self.tx_end_date.setDisplayFormat("yyyy-MM-dd")
        self.tx_end_date.setDate(QDate.currentDate())
        self.tx_end_date.setFixedWidth(140)
        filter_layout.addWidget(self.tx_end_date)

        filter_layout.addWidget(QLabel("类型"))
        self.tx_type_filter = QComboBox()
        self.tx_type_filter.addItems(["全部", "收入", "支出"])
        self.tx_type_filter.setFixedWidth(80)
        filter_layout.addWidget(self.tx_type_filter)

        filter_layout.addWidget(QLabel("分类"))
        self.tx_cat_filter = QComboBox()
        self.tx_cat_filter.addItem("全部", None)
        for cat in self.db.get_categories():
            self.tx_cat_filter.addItem(f"{cat['icon']} {cat['name']}", cat['id'])
        self.tx_cat_filter.setFixedWidth(130)
        filter_layout.addWidget(self.tx_cat_filter)

        query_btn = QPushButton("🔍 查询")
        query_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #40a9ff; }
        """)
        query_btn.clicked.connect(self.refresh_transactions)
        filter_layout.addWidget(query_btn)

        filter_layout.addStretch()

        add_btn = QPushButton("＋ 记一笔")
        add_btn.setObjectName("add_btn")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.on_add_transaction)
        filter_layout.addWidget(add_btn)

        layout.addLayout(filter_layout)

        summary_row = QHBoxLayout()
        self.tx_summary_label = QLabel("")
        self.tx_summary_label.setStyleSheet("color: #595959; font-size: 13px; padding: 4px 0;")
        summary_row.addWidget(self.tx_summary_label)
        summary_row.addStretch()
        layout.addLayout(summary_row)

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

    def refresh_transactions(self):
        start = self.tx_start_date.date().toString("yyyy-MM-dd")
        end = self.tx_end_date.date().toString("yyyy-MM-dd")
        type_idx = self.tx_type_filter.currentIndex()
        type_map = {0: None, 1: 'income', 2: 'expense'}
        tx_type = type_map[type_idx]
        cat_id = self.tx_cat_filter.currentData()

        transactions = self.db.get_transactions(
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
        del_btn.clicked.connect(lambda checked, tid=t['id']: self.on_delete_transaction(tid))
        self.tx_table.setCellWidget(row, 6, del_btn)

    def on_add_transaction(self):
        dialog = TransactionDialog(self.db, parent=self)
        if dialog.exec() == TransactionDialog.Accepted:
            data = dialog.get_data()
            self.db.add_transaction(**data)
            self.refresh_transactions()
            self.refresh_dashboard()

    def on_edit_transaction(self, t):
        dialog = TransactionDialog(self.db, transaction=t, parent=self)
        if dialog.exec() == TransactionDialog.Accepted:
            data = dialog.get_data()
            self.db.update_transaction(t['id'], **data)
            self.refresh_transactions()
            self.refresh_dashboard()

    def on_delete_transaction(self, tid):
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这条记录吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_transaction(tid)
            self.refresh_transactions()
            self.refresh_dashboard()

    # ==================== Statistics Page ====================
    def create_statistics_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.addWidget(QLabel("统计周期"))

        self.stat_year = QComboBox()
        current_year = date.today().year
        for y in range(current_year - 3, current_year + 1):
            self.stat_year.addItem(str(y), y)
        self.stat_year.setCurrentText(str(current_year))
        self.stat_year.setFixedWidth(100)
        header.addWidget(self.stat_year)

        header.addWidget(QLabel("年"))

        self.stat_month = QComboBox()
        for m in range(1, 13):
            self.stat_month.addItem(str(m), m)
        self.stat_month.setCurrentIndex(date.today().month - 1)
        self.stat_month.setFixedWidth(80)
        header.addWidget(self.stat_month)

        header.addWidget(QLabel("月"))

        query_btn = QPushButton("🔍 查询")
        query_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #40a9ff; }
        """)
        query_btn.clicked.connect(self.refresh_statistics)
        header.addWidget(query_btn)

        header.addStretch()
        layout.addLayout(header)

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
        year = self.stat_year.currentData()
        month = self.stat_month.currentData()
        if year is None:
            return

        start = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end = f"{year+1:04d}-01-01"
        else:
            end = f"{year:04d}-{month+1:02d}-01"

        summary = self.db.get_summary(start, end)
        self.stat_income_card._value_label.setText(f"¥ {summary['total_income']:,.2f}")
        self.stat_expense_card._value_label.setText(f"¥ {summary['total_expense']:,.2f}")
        self.stat_balance_card._value_label.setText(f"¥ {summary['balance']:,.2f}")

        tx_type = 'income' if self.stat_tab_income.isChecked() else 'expense'
        categories = self.db.get_category_summary(start, end, tx_type)

        for i in reversed(range(self.stat_content_layout.count())):
            item = self.stat_content_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        total = sum(c['total'] for c in categories) if categories else 0

        if not categories:
            empty = QLabel("暂无数据")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #8c8c8c; font-size: 14px; padding: 40px;")
            self.stat_content_layout.addWidget(empty)
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

            icon_label = QLabel(cat.get('icon', '📁'))
            icon_label.setFont(QFont("", 18))
            row_layout.addWidget(icon_label)

            name_layout = QVBoxLayout()
            name_label = QLabel(cat['name'])
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

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)
