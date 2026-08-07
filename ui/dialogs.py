from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QGridLayout, QWidget, QFrame,
    QDoubleSpinBox, QButtonGroup, QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from datetime import date


class TransactionDialog(QDialog):
    def __init__(self, db, transaction=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.transaction = transaction
        self.selected_type = 'expense'
        self.selected_category_id = None
        self.setWindowTitle("编辑记账" if transaction else "新增记账")
        self.setMinimumWidth(450)
        self.setup_ui()
        if transaction:
            self.load_transaction(transaction)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("编辑记账" if self.transaction else "新增记账")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        type_layout = QHBoxLayout()
        type_layout.setSpacing(12)

        self.type_group = QButtonGroup(self)
        self.btn_income = QPushButton("💵 收入")
        self.btn_expense = QPushButton("💸 支出")
        self.btn_income.setObjectName("type_income")
        self.btn_expense.setObjectName("type_expense")
        self.btn_income.setCheckable(True)
        self.btn_expense.setCheckable(True)
        self.btn_expense.setChecked(True)
        self.type_group.addButton(self.btn_income)
        self.type_group.addButton(self.btn_expense)
        type_layout.addWidget(self.btn_income)
        type_layout.addWidget(self.btn_expense)
        layout.addLayout(type_layout)

        self.btn_income.clicked.connect(lambda: self.on_type_changed('income'))
        self.btn_expense.clicked.connect(lambda: self.on_type_changed('expense'))

        form_layout = QGridLayout()
        form_layout.setSpacing(12)

        form_layout.addWidget(self.make_label("金额"), 0, 0)
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 99999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("¥ ")
        self.amount_input.setFont(QFont("", 14))
        form_layout.addWidget(self.amount_input, 0, 1)

        form_layout.addWidget(self.make_label("分类"), 1, 0)
        self.category_combo = QComboBox()
        form_layout.addWidget(self.category_combo, 1, 1)

        form_layout.addWidget(self.make_label("日期"), 2, 0)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addWidget(self.date_input, 2, 1)

        form_layout.addWidget(self.make_label("备注"), 3, 0)
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("输入备注信息（可选）")
        form_layout.addWidget(self.note_input, 3, 1)

        layout.addLayout(form_layout)
        self.update_categories()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #595959;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover { background-color: #d9d9d9; }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("保存")
        save_btn.setObjectName("add_btn")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover { background-color: #40a9ff; }
        """)
        save_btn.clicked.connect(self.on_save)

        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def make_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("", 13))
        label.setStyleSheet("color: #595959;")
        return label

    def on_type_changed(self, t):
        self.selected_type = t
        self.update_categories()

    def update_categories(self):
        self.category_combo.clear()
        categories = self.db.get_categories(type=self.selected_type)
        for cat in categories:
            self.category_combo.addItem(f"{cat['icon']} {cat['name']}", cat['id'])
        if categories:
            self.selected_category_id = categories[0]['id']
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)

    def on_category_changed(self, index):
        self.selected_category_id = self.category_combo.itemData(index)

    def load_transaction(self, t):
        if t['type'] == 'income':
            self.btn_income.setChecked(True)
        else:
            self.btn_expense.setChecked(True)
        self.selected_type = t['type']
        self.update_categories()

        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == t['category_id']:
                self.category_combo.setCurrentIndex(i)
                break

        self.amount_input.setValue(t['amount'])
        qdate = QDate.fromString(t['date'], "yyyy-MM-dd")
        self.date_input.setDate(qdate)
        self.note_input.setText(t.get('note', ''))

    def on_save(self):
        if self.amount_input.value() <= 0:
            QMessageBox.warning(self, "提示", "请输入有效金额")
            return
        self.accept()

    def get_data(self):
        return {
            'type': self.selected_type,
            'amount': self.amount_input.value(),
            'category_id': self.category_combo.currentData(),
            'date': self.date_input.date().toString("yyyy-MM-dd"),
            'note': self.note_input.text().strip()
        }
