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

QComboBox#txTypeFilter {
    background-color: #ffffff;
    color: #595959;
    border: 1px solid #d9d9d9;
    border-radius: 7px;
    padding: 0 30px 0 12px;
    font-size: 13px;
    font-weight: 500;
}

QComboBox#txTypeFilter:hover {
    background-color: #fafdff;
    border-color: #69b1ff;
}

QComboBox#txTypeFilter:focus,
QComboBox#txTypeFilter[filterType="all"]:focus {
    border: 2px solid #4096ff;
}

QComboBox#txTypeFilter[filterType="income"] {
    background-color: #f6ffed;
    color: #389e0d;
    border-color: #95de64;
    font-weight: bold;
}

QComboBox#txTypeFilter[filterType="income"]:focus {
    border: 2px solid #52c41a;
}

QComboBox#txTypeFilter[filterType="expense"] {
    background-color: #fff1f0;
    color: #cf1322;
    border-color: #ffaaa5;
    font-weight: bold;
}

QComboBox#txTypeFilter[filterType="expense"]:focus {
    border: 2px solid #ff4d4f;
}

QComboBox#txTypeFilter::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border: none;
    border-left: 1px solid rgba(0, 0, 0, 18);
}

QComboBox#txTypeFilter QAbstractItemView {
    background-color: #ffffff;
    color: #595959;
    border: 1px solid #d9e2ec;
    border-radius: 7px;
    padding: 5px;
    outline: none;
    selection-background-color: #e6f7ff;
    selection-color: #1677ff;
}

QComboBox#txTypeFilter QAbstractItemView::item {
    min-height: 32px;
    padding: 0 10px;
    border-radius: 5px;
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

QWidget#amountInput {
    background-color: #ffffff;
    border: 1px solid #d9d9d9;
    border-radius: 9px;
}

QWidget#amountInput[focused="true"] {
    border: 2px solid #1890ff;
}

QWidget#amountInput[error="true"] {
    border: 2px solid #ff4d4f;
    background-color: #fffafa;
}

QLabel#amountCurrency {
    color: #8c8c8c;
    font-size: 22px;
    font-weight: bold;
}

QLineEdit#amountEditor {
    background-color: transparent;
    border: none;
    padding: 0;
    min-height: 44px;
    color: #1a1a1a;
    font-size: 25px;
    font-weight: bold;
}

QPushButton#amountShortcut {
    background-color: #f7f9fc;
    color: #595959;
    border: 1px solid #e8e8e8;
    border-radius: 6px;
    padding: 5px 11px;
    font-size: 12px;
}

QPushButton#amountShortcut:hover {
    background-color: #e6f7ff;
    border-color: #91d5ff;
    color: #1890ff;
}

QPushButton#amountShortcut:pressed {
    background-color: #bae7ff;
}

QLabel#amountError {
    color: #ff4d4f;
    font-size: 12px;
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

/* Forest grocery ledger theme */
QMainWindow, QWidget#mainWorkspace, QWidget#contentWorkspace {
    background-color: #f3eadb;
    color: #292621;
}

QFrame#sidebar {
    background-color: #315f4c;
    border: none;
}

QLabel#sidebarBrand {
    color: #fff8e9;
    font-size: 20px;
    font-weight: bold;
    padding-top: 20px;
}

QLabel#sidebarSubtitle {
    color: #b9cebf;
    font-size: 9px;
    font-weight: bold;
    letter-spacing: 2px;
}

QPushButton#nav_btn {
    background-color: transparent;
    color: #dce8df;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 12px 22px;
    margin: 2px 12px;
    font-size: 14px;
}

QPushButton#nav_btn:hover {
    background-color: rgba(255, 253, 248, 28);
    color: #fffdf8;
}

QPushButton#nav_btn:checked {
    background-color: #f4e8d3;
    color: #315f4c;
    border: none;
    border-left: 4px solid #d4a64e;
    padding-left: 18px;
    font-weight: bold;
}

QLabel#storeStatus {
    background-color: rgba(255, 253, 248, 20);
    color: #d9c98f;
    border: 1px solid rgba(255, 253, 248, 34);
    border-radius: 8px;
    margin: 8px 14px;
    padding: 9px;
    font-size: 11px;
}

QFrame#mainHeader {
    background-color: #fffdf8;
    border: none;
    border-bottom: 1px solid #ded2bd;
}

QLabel#mainPageTitle {
    color: #292621;
    font-size: 17px;
    font-weight: bold;
}

QLabel#headerClock {
    color: #7c7468;
    font-size: 12px;
    margin-right: 16px;
}

QFrame#headerSeparator {
    color: #ded2bd;
}

QPushButton#accountButton {
    background-color: #faf6ed;
    color: #49443d;
    border: 1px solid #d8ccb7;
    border-radius: 7px;
    padding: 6px 14px;
    margin-left: 8px;
    font-size: 13px;
}

QPushButton#accountButton:hover {
    background-color: #edf3ed;
    border-color: #5e8a69;
    color: #315f4c;
}

QPushButton#accountButton::menu-indicator {
    image: none;
    width: 0;
}

QMenu#accountMenu {
    background-color: #fffdf8;
    border: 1px solid #ded2bd;
    border-radius: 8px;
    padding: 6px;
}

QMenu#accountMenu::item {
    color: #49443d;
    padding: 9px 30px 9px 14px;
    border-radius: 6px;
}

QMenu#accountMenu::item:selected {
    background-color: #e3ece5;
    color: #315f4c;
}

QMenu#accountMenu::separator {
    height: 1px;
    background-color: #e9e0d1;
    margin: 5px 8px;
}

QLabel#dashboard_title, QLabel#accountPageTitle, QLabel#notebookPageTitle {
    color: #292621;
    font-size: 17px;
    font-weight: bold;
    padding: 4px 0;
}

QLabel#notebookDescription {
    color: #7c7468;
    font-size: 12px;
    padding-bottom: 4px;
}

QLabel#notebookListEmpty {
    color: #8c8377;
    font-size: 13px;
    padding: 30px 12px;
}

QLineEdit#notebookSearch {
    background-color: #fffdf8;
}

QSplitter#notebookSplitter::handle {
    background-color: #e9e0d1;
    width: 1px;
}

QFrame#notebookListPanel, QFrame#notebookEditorPanel {
    background-color: #fffdf8;
    border: 1px solid #ded2bd;
    border-radius: 10px;
}

QListWidget#notebookList {
    background-color: transparent;
    border: none;
    outline: none;
    padding: 6px;
}

QListWidget#notebookList::item {
    background-color: #faf6ed;
    border: 1px solid #e4d9c6;
    border-radius: 8px;
}

QListWidget#notebookList::item:hover {
    background-color: #f3ecdf;
    border-color: #c8bca8;
}

QListWidget#notebookList::item:selected {
    background-color: #e3ece5;
    border-color: #5e8a69;
}

QLabel#notebookCardTitle {
    color: #292621;
    font-size: 13px;
    font-weight: bold;
}

QLabel#notebookCardUpdateTime {
    color: #9b9286;
    font-size: 11px;
}

QLabel#notebookDateHeader, QLabel#notebookDateHeaderToday {
    color: #8c8377;
    font-size: 11px;
    font-weight: bold;
}

QLabel#notebookDateHeaderToday {
    color: #315f4c;
}

QLabel#notebookEditorHint, QLabel#notebookSaveState {
    color: #948a7b;
    font-size: 11px;
}

QLineEdit#notebookEditorTitle {
    background-color: transparent;
    color: #292621;
    border: none;
    border-bottom: 1px solid #e4d9c6;
    border-radius: 0;
    padding: 6px 2px;
    font-size: 19px;
    font-weight: bold;
}

QLineEdit#notebookEditorTitle:focus {
    border-bottom-color: #5e8a69;
}

QTextEdit#notebookEditorContent {
    background-color: #fffdf8;
    color: #292621;
    border: none;
    padding: 4px 2px;
    font-size: 13px;
}

QFrame#notebookEditorPanel:disabled {
    background-color: #faf6ed;
}

QPushButton#notebookCancelButton {
    background-color: #faf6ed;
    color: #49443d;
    border: 1px solid #d8ccb7;
    border-radius: 7px;
}

QPushButton#notebookCancelButton:hover {
    background-color: #ede5d7;
}

QPushButton#notebookSaveButton {
    background-color: #315f4c;
    color: #fffdf8;
    border: 1px solid #315f4c;
    border-radius: 7px;
    font-weight: bold;
}

QPushButton#notebookSaveButton:hover {
    background-color: #3d745d;
}

QPushButton#notebookSaveButton:disabled,
QPushButton#notebookCancelButton:disabled {
    background-color: #ede8de;
    color: #aaa195;
    border-color: #d8d0c4;
}

QLabel#dashboard_section_title {
    color: #49443d;
    font-size: 14px;
    font-weight: bold;
}

QFrame#dashboard_panel {
    background-color: #fffdf8;
    border: 1px solid #ded2bd;
    border-radius: 12px;
}

QFrame#dashboard_card_income {
    background-color: #edf4eb;
    border: 1px solid #bdd0b9;
}

QFrame#dashboard_card_expense {
    background-color: #faece6;
    border: 1px solid #dfb6a8;
}

QFrame#dashboard_card_balance {
    background-color: #fbf1d8;
    border: 1px solid #e0c785;
}

QFrame#dashboard_card_count {
    background-color: #e8f0ed;
    border: 1px solid #b5cbc4;
}

QLabel#dashboard_card_title, QLabel#dashboard_card_detail, QLabel#stat_title {
    color: #7c7468;
}

QLabel#dashboard_value_income, QLabel#stat_value_income {
    color: #5e8a69;
}

QLabel#dashboard_value_expense, QLabel#stat_value_expense {
    color: #b85f45;
}

QLabel#dashboard_value_balance, QLabel#stat_value_balance {
    color: #9b742c;
}

QLabel#dashboard_value_count {
    color: #5b8982;
}

QPushButton#link_btn {
    background-color: transparent;
    color: #315f4c;
    border: none;
}

QPushButton#link_btn:hover {
    color: #5e8a69;
    text-decoration: underline;
}

QLabel#dashboard_empty, QLabel#statisticsEmpty {
    color: #948a7b;
    font-size: 13px;
    padding: 40px;
}

QLabel#dashboard_category_name {
    color: #49443d;
}

QLabel#dashboard_category_amount {
    color: #b85f45;
}

QProgressBar#dashboard_category_progress {
    background-color: #ede5d7;
}

QProgressBar#dashboard_category_progress::chunk {
    background-color: #b85f45;
}

QFrame#stat_card_income {
    background-color: #edf4eb;
    border: 1px solid #bdd0b9;
}

QFrame#stat_card_expense {
    background-color: #faece6;
    border: 1px solid #dfb6a8;
}

QFrame#stat_card_balance {
    background-color: #fbf1d8;
    border: 1px solid #e0c785;
}

QFrame#filterBar {
    background-color: #fffdf8;
    border: 1px solid #ded2bd;
    border-radius: 10px;
}

QLabel#filter_label {
    color: #7c7468;
}

QPushButton#dateRangePicker, QPushButton#monthPicker,
QComboBox, QDateEdit, QLineEdit, QSpinBox {
    background-color: #fffdf8;
    color: #292621;
    border: 1px solid #d8ccb7;
    border-radius: 7px;
}

QPushButton#dateRangePicker:hover, QPushButton#monthPicker:hover,
QComboBox:hover, QDateEdit:hover, QLineEdit:hover, QSpinBox:hover {
    background-color: #ffffff;
    border-color: #5e8a69;
    color: #315f4c;
}

QComboBox:focus, QDateEdit:focus, QLineEdit:focus, QSpinBox:focus {
    border-color: #315f4c;
}

QComboBox QAbstractItemView {
    background-color: #fffdf8;
    border: 1px solid #d8ccb7;
    selection-background-color: #e3ece5;
    selection-color: #315f4c;
}

QComboBox#txTypeFilter {
    background-color: #fffdf8;
    color: #7c7468;
    border-color: #d8ccb7;
}

QComboBox#txTypeFilter:hover, QComboBox#txTypeFilter:focus,
QComboBox#txTypeFilter[filterType="all"]:focus {
    background-color: #ffffff;
    border: 1px solid #5e8a69;
}

QComboBox#txTypeFilter[filterType="income"] {
    background-color: #edf4eb;
    color: #5e8a69;
    border-color: #9fbc9f;
}

QComboBox#txTypeFilter[filterType="expense"] {
    background-color: #faece6;
    color: #b85f45;
    border-color: #d9a898;
}

QComboBox#txTypeFilter QAbstractItemView {
    background-color: #fffdf8;
    color: #49443d;
    border-color: #d8ccb7;
    selection-background-color: #e3ece5;
    selection-color: #315f4c;
}

QPushButton#add_btn, QPushButton#account_add_btn, QPushButton#notebookAddButton {
    background: #315f4c;
    color: #fffdf8;
    border: 1px solid #315f4c;
    border-radius: 7px;
    font-weight: bold;
}

QPushButton#add_btn:hover, QPushButton#account_add_btn:hover, QPushButton#notebookAddButton:hover {
    background: #3d745d;
    border-color: #3d745d;
}

QPushButton#add_btn:pressed, QPushButton#account_add_btn:pressed, QPushButton#notebookAddButton:pressed {
    background: #244c3c;
    border-color: #244c3c;
}

QPushButton#query_btn {
    background-color: #faf6ed;
    color: #49443d;
    border: 1px solid #d8ccb7;
    border-radius: 7px;
}

QPushButton#query_btn:hover {
    background-color: #e3ece5;
    color: #315f4c;
    border-color: #5e8a69;
}

QPushButton#edit_btn, QPushButton#accountEditButton, QPushButton#notebookEditButton {
    background-color: #fbf1d8;
    color: #8b6828;
    border: 1px solid #d9bd73;
    border-radius: 6px;
}

QPushButton#edit_btn:hover, QPushButton#accountEditButton:hover, QPushButton#notebookEditButton:hover {
    background-color: #f2dfa9;
}

QPushButton#delete_btn, QPushButton#accountDeleteButton {
    background-color: #fff4ef;
    color: #a84f3c;
    border: 1px solid #d99a88;
    border-radius: 6px;
}

QPushButton#delete_btn:hover, QPushButton#accountDeleteButton:hover {
    background-color: #b85f45;
    color: #fffdf8;
}

QPushButton#accountDeleteButton:disabled {
    background-color: #f1ede5;
    color: #aaa195;
    border-color: #d8d0c4;
}

QTableWidget {
    background-color: #fffdf8;
    alternate-background-color: #faf6ed;
    color: #292621;
    border: 1px solid #ded2bd;
    gridline-color: #ebe2d4;
    selection-background-color: #e3ece5;
}

QTableWidget::item:selected {
    background-color: #e3ece5;
    color: #292621;
}

QHeaderView::section {
    background-color: #f0e6d5;
    color: #49443d;
    border: none;
    border-bottom: 1px solid #d8ccb7;
}

QPushButton#statTypeTab {
    background-color: #faf6ed;
    color: #7c7468;
    border: 1px solid #d8ccb7;
    border-radius: 7px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#statTypeTab:hover {
    color: #315f4c;
    border-color: #5e8a69;
}

QPushButton#statTypeTab:checked {
    background-color: #315f4c;
    color: #fffdf8;
    border-color: #315f4c;
}

QFrame#statisticsRow {
    background-color: #fffdf8;
    border: 1px solid #e4d9c6;
    border-radius: 10px;
}

QLabel#statisticsName {
    color: #292621;
}

QScrollBar::handle:vertical {
    background-color: #c8bca8;
}

QScrollBar::handle:vertical:hover {
    background-color: #a99c88;
}

QToolTip {
    background-color: #315f4c;
    color: #fffdf8;
    border: 1px solid #244c3c;
    padding: 5px;
}
"""
