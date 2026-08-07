MAIN_STYLE = """
QMainWindow {
    background-color: #f0f2f5;
}

QFrame#sidebar {
    background-color: #ffffff;
    border: none;
}

QPushButton#nav_btn {
    background-color: transparent;
    color: #595959;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 8px;
    margin: 2px 8px;
}

QPushButton#nav_btn:hover {
    background-color: #f0f2f5;
    color: #1890ff;
}

QPushButton#nav_btn:checked {
    background-color: #e6f7ff;
    color: #1890ff;
    font-weight: bold;
    border-left: 3px solid #1890ff;
    padding-left: 17px;
}

QFrame#content_area {
    background-color: #ffffff;
    border-radius: 12px;
    margin: 8px;
    padding: 16px;
}

QLabel#page_title {
    font-size: 20px;
    font-weight: bold;
    color: #1a1a1a;
    padding: 4px 0;
    margin-bottom: 12px;
}

QLabel#dashboard_title {
    color: #1a1a1a;
    font-size: 17px;
    font-weight: bold;
}

QLabel#dashboard_section_title {
    color: #1a1a1a;
    font-size: 14px;
    font-weight: bold;
}

QFrame#dashboard_panel {
    background-color: #ffffff;
    border: 1px solid #edf0f5;
    border-radius: 12px;
}

QFrame#dashboard_card_income,
QFrame#dashboard_card_expense,
QFrame#dashboard_card_balance,
QFrame#dashboard_card_count {
    border-radius: 12px;
    min-height: 78px;
}

QFrame#dashboard_card_income {
    background-color: #f6ffed;
    border: 1px solid #b7eb8f;
}

QFrame#dashboard_card_expense {
    background-color: #fff1f0;
    border: 1px solid #ffa39e;
}

QFrame#dashboard_card_balance {
    background-color: #e6f7ff;
    border: 1px solid #91d5ff;
}

QFrame#dashboard_card_count {
    background-color: #fffbe6;
    border: 1px solid #ffe58f;
}

QLabel#dashboard_card_title {
    color: #8c8c8c;
    font-size: 12px;
}

QLabel#dashboard_value_income,
QLabel#dashboard_value_expense,
QLabel#dashboard_value_balance,
QLabel#dashboard_value_count {
    font-size: 21px;
    font-weight: bold;
}

QLabel#dashboard_value_income {
    color: #389e0d;
}

QLabel#dashboard_value_expense {
    color: #cf1322;
}

QLabel#dashboard_value_balance {
    color: #096dd9;
}

QLabel#dashboard_value_count {
    color: #d48806;
}

QLabel#dashboard_card_detail {
    color: #8c8c8c;
    font-size: 11px;
}

QPushButton#link_btn {
    background-color: transparent;
    color: #1890ff;
    border: none;
    padding: 4px 8px;
    font-size: 12px;
}

QPushButton#link_btn:hover {
    color: #40a9ff;
    text-decoration: underline;
}

QLabel#dashboard_empty {
    color: #bfbfbf;
    font-size: 13px;
    padding: 50px 0;
}

QLabel#dashboard_category_name {
    color: #595959;
    font-size: 12px;
}

QLabel#dashboard_category_amount {
    color: #f5222d;
    font-size: 12px;
    font-weight: bold;
}

QProgressBar#dashboard_category_progress {
    background-color: #f0f0f0;
    border: none;
    border-radius: 3px;
    min-height: 6px;
    max-height: 6px;
}

QProgressBar#dashboard_category_progress::chunk {
    background-color: #ff7875;
    border-radius: 3px;
}

QFrame#stat_card {
    background-color: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 20px;
    min-width: 180px;
}

QFrame#stat_card_income {
    background-color: #f6ffed;
    border: 1px solid #b7eb8f;
    border-radius: 12px;
    padding: 20px;
    min-width: 180px;
}

QFrame#stat_card_expense {
    background-color: #fff1f0;
    border: 1px solid #ffa39e;
    border-radius: 12px;
    padding: 20px;
    min-width: 180px;
}

QFrame#stat_card_balance {
    background-color: #e6f7ff;
    border: 1px solid #91d5ff;
    border-radius: 12px;
    padding: 20px;
    min-width: 180px;
}

QLabel#stat_title {
    font-size: 12px;
    color: #8c8c8c;
}

QLabel#stat_value_income {
    font-size: 24px;
    font-weight: bold;
    color: #52c41a;
}

QLabel#stat_value_expense {
    font-size: 24px;
    font-weight: bold;
    color: #f5222d;
}

QLabel#stat_value_balance {
    font-size: 24px;
    font-weight: bold;
    color: #1890ff;
}

QPushButton#query_btn {
    background-color: #ffffff;
    color: #1890ff;
    border: 1px solid #1890ff;
    border-radius: 6px;
    padding: 0 12px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#query_btn:hover {
    background-color: #e6f7ff;
    border-color: #40a9ff;
    color: #40a9ff;
}

QPushButton#query_btn:pressed {
    background-color: #bae7ff;
}

QFrame#filterBar {
    background-color: #fafafa;
    border: 1px solid #f0f0f0;
    border-radius: 10px;
}

QFrame#filterBar QDateEdit, QFrame#filterBar QComboBox {
    padding: 0 8px;
    min-height: 38px;
    max-height: 38px;
}

QPushButton#dateRangePicker {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #d9d9d9;
    border-radius: 6px;
    padding: 0 12px;
    text-align: left;
    font-size: 13px;
}

QPushButton#dateRangePicker:hover {
    background-color: #fafdff;
    border-color: #40a9ff;
    color: #1890ff;
}

QPushButton#dateRangePicker:pressed {
    background-color: #e6f7ff;
}

QPushButton#monthPicker {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #d9d9d9;
    border-radius: 6px;
    padding: 0 12px;
    text-align: left;
    font-size: 13px;
}

QPushButton#monthPicker:hover {
    background-color: #fafdff;
    border-color: #40a9ff;
    color: #1890ff;
}

QPushButton#monthPicker:pressed {
    background-color: #e6f7ff;
}

QLabel#filter_label {
    color: #8c8c8c;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#add_btn {
    background-color: #1890ff;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0 12px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#add_btn:hover {
    background-color: #40a9ff;
}

QPushButton#add_btn:pressed {
    background-color: #096dd9;
}

QPushButton#account_add_btn {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #40a9ff, stop: 1 #1677ff
    );
    color: #ffffff;
    border: 1px solid #1677ff;
    border-radius: 9px;
    padding: 0 18px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#account_add_btn:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #69bfff, stop: 1 #4096ff
    );
    border-color: #4096ff;
}

QPushButton#account_add_btn:pressed {
    background-color: #0958d9;
    border-color: #0958d9;
    padding-top: 1px;
}

QPushButton#account_add_btn:focus {
    border: 2px solid #91caff;
}

QPushButton#delete_btn {
    background-color: #ff4d4f;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#delete_btn:hover {
    background-color: #ff7875;
}

QPushButton#edit_btn {
    background-color: #faad14;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#edit_btn:hover {
    background-color: #ffc53d;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #f0f0f0;
    border-radius: 12px;
    gridline-color: #f0f0f0;
    font-size: 13px;
    selection-background-color: #e6f7ff;
    alternate-background-color: #fafafa;
}

QTableWidget::item {
    padding: 10px;
}

QTableWidget::item:selected {
    background-color: #e6f7ff;
    color: #1a1a1a;
}

QHeaderView::section {
    background-color: #fafafa;
    color: #595959;
    font-size: 13px;
    font-weight: bold;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #f0f0f0;
}

QComboBox, QDateEdit, QLineEdit, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #d9d9d9;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 14px;
    min-height: 32px;
    color: #1a1a1a;
}

QComboBox:focus, QDateEdit:focus, QLineEdit:focus, QSpinBox:focus {
    border-color: #1890ff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #d9d9d9;
    selection-background-color: #e6f7ff;
    selection-color: #1a1a1a;
}

QLabel#card_title {
    font-size: 15px;
    font-weight: bold;
    color: #1a1a1a;
    padding: 4px 0;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background-color: #d9d9d9;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #bfbfbf;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QPushButton#type_income {
    background-color: #f6ffed;
    color: #52c41a;
    border: 2px solid #b7eb8f;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: bold;
    min-height: 20px;
}

QPushButton#type_income:checked {
    background-color: #52c41a;
    color: #ffffff;
    border-color: #52c41a;
}

QPushButton#type_expense {
    background-color: #fff1f0;
    color: #f5222d;
    border: 2px solid #ffa39e;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: bold;
    min-height: 20px;
}

QPushButton#type_expense:checked {
    background-color: #f5222d;
    color: #ffffff;
    border-color: #f5222d;
}

QDialog {
    background-color: #ffffff;
}

QLabel#dialog_title {
    font-size: 18px;
    font-weight: bold;
    color: #1a1a1a;
    padding: 8px 0;
}

QFrame#category_item {
    background-color: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 4px;
    min-height: 40px;
}

QFrame#category_item:hover {
    border-color: #1890ff;
    background-color: #e6f7ff;
}

QFrame#category_item:selected {
    border-color: #1890ff;
    border-width: 2px;
    background-color: #e6f7ff;
}

QLabel#income_text {
    color: #52c41a;
    font-weight: bold;
}

QLabel#expense_text {
    color: #f5222d;
    font-weight: bold;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #f0f0f0;
    text-align: center;
    min-height: 12px;
    max-height: 12px;
}

QProgressBar::chunk {
    border-radius: 6px;
}

QTabWidget::pane {
    border: none;
    background-color: transparent;
}

QTabBar::tab {
    padding: 8px 16px;
    border: none;
    font-size: 14px;
    color: #595959;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:selected {
    color: #1890ff;
    border-bottom-color: #1890ff;
    font-weight: bold;
}

QTabBar::tab:hover {
    color: #1890ff;
}
"""
