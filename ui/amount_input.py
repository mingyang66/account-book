import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget


class AmountLineEdit(QLineEdit):
    focusChanged = Signal(bool)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusChanged.emit(True)
        self.selectAll()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focusChanged.emit(False)

    def insertFromMimeData(self, source):
        cleaned = AmountInput.clean_text(source.text())
        if cleaned:
            self.insert(cleaned)


class AmountInput(QWidget):
    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("amountInput")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(5)

        currency_label = QLabel("¥")
        currency_label.setObjectName("amountCurrency")
        layout.addWidget(currency_label)

        self.editor = AmountLineEdit()
        self.editor.setObjectName("amountEditor")
        self.editor.setPlaceholderText("0.00")
        self.editor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        validator = QDoubleValidator(0.0, 99999999.99, 2, self.editor)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.editor.setValidator(validator)
        self.editor.textChanged.connect(self._emit_value)
        self.editor.editingFinished.connect(self.format_value)
        self.editor.focusChanged.connect(self._set_focused)
        layout.addWidget(self.editor, 1)

    def value(self):
        text = self.clean_text(self.editor.text())
        try:
            return float(text) if text else 0.0
        except ValueError:
            return 0.0

    def setValue(self, amount):
        self.editor.setText(f"{float(amount):.2f}" if amount else "")

    def add_value(self, amount):
        self.setValue(min(self.value() + amount, 99999999.99))
        self.editor.setFocus()
        self.editor.selectAll()

    def set_error(self, has_error):
        self.setProperty("error", has_error)
        self.style().unpolish(self)
        self.style().polish(self)

    def focus_input(self):
        self.editor.setFocus()
        self.editor.selectAll()

    def format_value(self):
        amount = self.value()
        if amount > 0:
            self.editor.setText(f"{amount:.2f}")

    def _emit_value(self):
        self.set_error(False)
        self.valueChanged.emit(self.value())

    @staticmethod
    def clean_text(text):
        return re.sub(r"[^0-9.]", "", text.replace(",", ""))

    def _set_focused(self, focused):
        self.setProperty("focused", focused)
        self.style().unpolish(self)
        self.style().polish(self)
