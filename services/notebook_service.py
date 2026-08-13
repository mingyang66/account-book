from database import Database
from session import UserSession


class NotebookService:
    def __init__(self, database: Database, session: UserSession):
        self.database = database
        self.session = session

    def get_notebooks(self, keyword: str = ""):
        return self.database.get_notebooks(
            self.session.accountcode, keyword.strip()
        )

    def get_notebook(self, notebook_id: int):
        return self.database.get_notebook(self.session.accountcode, notebook_id)

    def add_notebook(self, title: str, content: str) -> tuple[bool, str]:
        title = title.strip()
        if not title:
            return False, "记事本标题不能为空"
        if len(title) > 64:
            return False, "记事本标题不能超过64个字符"
        self.database.add_notebook(self.session.accountcode, title, content.strip())
        return True, "新增成功"

    def update_notebook(
        self, notebook_id: int, title: str, content: str
    ) -> tuple[bool, str]:
        title = title.strip()
        if not title:
            return False, "记事本标题不能为空"
        if len(title) > 64:
            return False, "记事本标题不能超过64个字符"
        updated = self.database.update_notebook(
            self.session.accountcode, notebook_id, title, content.strip()
        )
        if not updated:
            return False, "记事本不存在或无权修改"
        return True, "修改成功"
