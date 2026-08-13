from datetime import date, datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ElidedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._full_text = text
        self.setToolTip(text)
        self.setMinimumWidth(0)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        elided = self.fontMetrics().elidedText(
            self._full_text, Qt.ElideRight, self.width()
        )
        super().setText(elided)


class NotebookCard(QWidget):
    def __init__(self, notebook, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 9, 12, 9)

        title = ElidedLabel(notebook["title"])
        title.setObjectName("notebookCardTitle")
        layout.addWidget(title, 1)

        update_time = QLabel(NotebookPage.format_update_time(notebook["updateTime"]))
        update_time.setObjectName("notebookCardUpdateTime")
        layout.addWidget(update_time)


class NotebookDateHeader(QLabel):
    def __init__(self, text, is_today=False, parent=None):
        super().__init__(text, parent)
        self.setObjectName(
            "notebookDateHeaderToday" if is_today else "notebookDateHeader"
        )
        self.setContentsMargins(8, 8, 4, 2)


class NotebookPage(QWidget):
    def __init__(self, notebook_service, parent=None):
        super().__init__(parent)
        self.notebook_service = notebook_service
        self.notebooks = []
        self.current_notebook = None
        self._dirty = False
        self._changing_selection = False
        self.setup_ui()
        self.refresh_notebooks(select_first=True)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 12, 24, 16)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("我的记事本")
        title.setObjectName("notebookPageTitle")
        header.addWidget(title)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setObjectName("notebookSearch")
        self.search_input.setPlaceholderText("搜索标题或内容")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedSize(220, 38)
        self.search_input.textChanged.connect(self.on_search_changed)
        header.addWidget(self.search_input)

        self.add_button = QPushButton("＋  新建记事本")
        self.add_button.setObjectName("notebookAddButton")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.setFixedSize(132, 38)
        self.add_button.clicked.connect(self.on_add_notebook)
        header.addWidget(self.add_button)
        layout.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setObjectName("notebookSplitter")
        splitter.setChildrenCollapsible(False)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        list_panel = QFrame()
        list_panel.setObjectName("notebookListPanel")
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("notebookList")
        self.list_widget.setSpacing(4)
        self.list_widget.currentItemChanged.connect(self.on_selection_changed)
        list_layout.addWidget(self.list_widget)

        self.list_empty_label = QLabel("暂无记事本\n点击“新建记事本”开始记录")
        self.list_empty_label.setObjectName("notebookListEmpty")
        self.list_empty_label.setAlignment(Qt.AlignCenter)
        list_layout.addWidget(self.list_empty_label)
        splitter.addWidget(list_panel)

        self.editor_panel = QFrame()
        self.editor_panel.setObjectName("notebookEditorPanel")
        editor_layout = QVBoxLayout(self.editor_panel)
        editor_layout.setContentsMargins(22, 20, 22, 18)
        editor_layout.setSpacing(12)

        editor_header = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setObjectName("notebookEditorTitle")
        self.title_input.setPlaceholderText("输入记事本标题")
        self.title_input.setMaxLength(64)
        self.title_input.textChanged.connect(self.mark_dirty)
        editor_header.addWidget(self.title_input)

        self.save_state = QLabel("")
        self.save_state.setObjectName("notebookSaveState")
        editor_header.addWidget(self.save_state)
        editor_layout.addLayout(editor_header)

        self.content_input = QTextEdit()
        self.content_input.setObjectName("notebookEditorContent")
        self.content_input.setPlaceholderText(
            "记录经营备忘、进货清单或待办事项..."
        )
        self.content_input.textChanged.connect(self.mark_dirty)
        editor_layout.addWidget(self.content_input)

        actions = QHBoxLayout()
        self.editor_hint = QLabel("Ctrl+S 保存")
        self.editor_hint.setObjectName("notebookEditorHint")
        actions.addWidget(self.editor_hint)
        actions.addStretch()

        self.cancel_button = QPushButton("取消修改")
        self.cancel_button.setObjectName("notebookCancelButton")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setFixedSize(92, 38)
        self.cancel_button.clicked.connect(self.on_cancel_edit)
        actions.addWidget(self.cancel_button)

        self.save_button = QPushButton("保存")
        self.save_button.setObjectName("notebookSaveButton")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setFixedSize(92, 38)
        self.save_button.clicked.connect(self.save_current)
        actions.addWidget(self.save_button)
        editor_layout.addLayout(actions)
        splitter.addWidget(self.editor_panel)

        splitter.setSizes([300, 650])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)

        QShortcut(QKeySequence.Save, self, activated=self.save_current)
        QShortcut(QKeySequence.New, self, activated=self.on_add_notebook)
        self.set_editor_enabled(False)

    def refresh_notebooks(self, selected_id=None, select_first=False):
        keyword = self.search_input.text().strip()
        self.notebooks = self.notebook_service.get_notebooks(keyword)
        self._changing_selection = True
        self.list_widget.clear()

        selected_item = None
        first_notebook_item = None
        current_group = None
        for notebook in self.notebooks:
            created_date = self.parse_timestamp(notebook["createTime"]).date()
            if created_date != current_group:
                current_group = created_date
                header_item = QListWidgetItem()
                header_item.setFlags(Qt.NoItemFlags)
                header = NotebookDateHeader(
                    self.format_date_group(created_date),
                    created_date == date.today(),
                )
                header_item.setSizeHint(header.sizeHint())
                self.list_widget.addItem(header_item)
                self.list_widget.setItemWidget(header_item, header)

            item = QListWidgetItem()
            item.setData(Qt.UserRole, notebook["id"])
            item.setSizeHint(NotebookCard(notebook).sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, NotebookCard(notebook))
            if first_notebook_item is None:
                first_notebook_item = item
            if notebook["id"] == selected_id:
                selected_item = item

        if selected_item is not None:
            self.list_widget.setCurrentItem(selected_item)
        elif select_first and first_notebook_item is not None:
            selected_item = first_notebook_item
            self.list_widget.setCurrentItem(selected_item)
        self._changing_selection = False

        has_results = bool(self.notebooks)
        self.list_widget.setVisible(has_results)
        self.list_empty_label.setVisible(not has_results)
        self.list_empty_label.setText(
            "未找到匹配的记事本" if keyword
            else "暂无记事本\n点击“新建记事本”开始记录"
        )

        if selected_item is not None and not self._dirty:
            self.load_notebook(self.notebook_by_id(selected_item.data(Qt.UserRole)))

    def notebook_by_id(self, notebook_id):
        return next(
            (item for item in self.notebooks if item["id"] == notebook_id), None
        )

    @staticmethod
    def parse_timestamp(value):
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            return datetime.min

    @staticmethod
    def format_date_group(created_date):
        today = date.today()
        if created_date == today:
            return f"今天 · {created_date.month}月{created_date.day}日"
        if created_date == today - timedelta(days=1):
            return f"昨天 · {created_date.month}月{created_date.day}日"
        if created_date.year == today.year:
            return f"{created_date.month}月{created_date.day}日"
        return f"{created_date.year}年{created_date.month}月{created_date.day}日"

    @staticmethod
    def format_update_time(value):
        updated_at = NotebookPage.parse_timestamp(value)
        return updated_at.strftime("%H:%M") if updated_at != datetime.min else ""

    def on_search_changed(self):
        current_id = self.current_notebook["id"] if self.current_notebook else None
        self.refresh_notebooks(selected_id=current_id)

    def on_selection_changed(self, current, previous):
        if self._changing_selection or current is None:
            return
        notebook_id = current.data(Qt.UserRole)
        if self.current_notebook and self.current_notebook.get("id") == notebook_id:
            return
        if not self.resolve_unsaved_changes():
            self.restore_selection(previous)
            return
        notebook = self.notebook_service.get_notebook(notebook_id)
        if notebook is None:
            QMessageBox.warning(self, "提示", "记事本不存在或已被移除")
            self.refresh_notebooks(select_first=True)
            return
        self.load_notebook(notebook)

    def restore_selection(self, item):
        self._changing_selection = True
        self.list_widget.setCurrentItem(item)
        self._changing_selection = False

    def load_notebook(self, notebook):
        if notebook is None:
            self.clear_editor()
            return
        self.current_notebook = notebook
        self.set_editor_enabled(True)
        self.title_input.blockSignals(True)
        self.content_input.blockSignals(True)
        self.title_input.setText(notebook["title"])
        self.content_input.setPlainText(notebook["content"])
        self.title_input.blockSignals(False)
        self.content_input.blockSignals(False)
        self.set_dirty(False)

    def on_add_notebook(self):
        if not self.resolve_unsaved_changes():
            return
        self._changing_selection = True
        self.list_widget.setCurrentItem(None)
        self._changing_selection = False
        self.current_notebook = {"id": None, "title": "", "content": ""}
        self.set_editor_enabled(True)
        self.title_input.clear()
        self.content_input.clear()
        self.set_dirty(False)
        self.save_state.setText("新建草稿")
        self.title_input.setFocus()

    def mark_dirty(self):
        if self.editor_panel.isEnabled():
            self.set_dirty(True)

    def set_dirty(self, dirty):
        self._dirty = dirty
        self.save_button.setEnabled(dirty or self.is_new_draft())
        self.cancel_button.setEnabled(dirty or self.is_new_draft())
        self.save_state.setText("未保存" if dirty else "已保存")

    def is_new_draft(self):
        return self.current_notebook is not None and self.current_notebook["id"] is None

    def save_current(self):
        if self.current_notebook is None:
            return False
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        if self.is_new_draft():
            success, message = self.notebook_service.add_notebook(title, content)
            if success:
                newest = self.notebook_service.get_notebooks()[0]
                self.current_notebook = newest
        else:
            success, message = self.notebook_service.update_notebook(
                self.current_notebook["id"], title, content
            )
            if success:
                self.current_notebook = self.notebook_service.get_notebook(
                    self.current_notebook["id"]
                )
        if not success:
            QMessageBox.warning(self, "保存失败", message)
            self.title_input.setFocus()
            return False

        self.set_dirty(False)
        self.refresh_notebooks(selected_id=self.current_notebook["id"])
        self.save_state.setText("已保存")
        return True

    def resolve_unsaved_changes(self):
        if not self._dirty and not self.is_new_draft():
            return True
        if self.is_new_draft() and not (
            self.title_input.text().strip() or self.content_input.toPlainText().strip()
        ):
            return True
        result = QMessageBox.question(
            self,
            "内容未保存",
            "当前记事本有未保存的修改，是否保存？",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save,
        )
        if result == QMessageBox.Save:
            return self.save_current()
        if result == QMessageBox.Discard:
            self.on_cancel_edit()
            return True
        return False

    def on_cancel_edit(self):
        if self.is_new_draft():
            self.current_notebook = None
            self.clear_editor()
            self.refresh_notebooks(select_first=True)
        elif self.current_notebook:
            notebook = self.notebook_service.get_notebook(
                self.current_notebook["id"]
            )
            self.load_notebook(notebook)

    def set_editor_enabled(self, enabled):
        self.editor_panel.setEnabled(enabled)
        self.title_input.setEnabled(enabled)
        self.content_input.setEnabled(enabled)
        self.save_button.setEnabled(enabled)
        self.cancel_button.setEnabled(enabled)

    def clear_editor(self):
        self.current_notebook = None
        self.title_input.blockSignals(True)
        self.content_input.blockSignals(True)
        self.title_input.clear()
        self.content_input.clear()
        self.title_input.blockSignals(False)
        self.content_input.blockSignals(False)
        self._dirty = False
        self.save_state.clear()
        self.set_editor_enabled(False)
