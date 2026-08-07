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
    min-height: 36px;
    max-height: 36px;
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
