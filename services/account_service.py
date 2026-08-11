from database import Database
from security import PasswordHasher


class AccountService:
    def __init__(self, database: Database, password_hasher: PasswordHasher):
        self.database = database
        self.password_hasher = password_hasher
        self.ensure_default_account()

    def ensure_default_account(self):
        if self.database.get_accounts():
            return
        self.database.insert_account(
            1000000, "admin", self.password_hasher.hash("123456")
        )

    def get_accounts(self):
        return self.database.get_accounts()

    def add_account(self, username: str, password: str) -> tuple[bool, str]:
        if not username:
            return False, "用户名不能为空"
        if not password or len(password) < 6:
            return False, "密码不能少于6位"
        if self.database.username_exists(username):
            return False, "用户名已存在"
        self.database.insert_account(
            self.database.get_next_accountcode(),
            username,
            self.password_hasher.hash(password),
        )
        return True, "添加成功"

    def update_account(
        self, account_id: int, username: str, password: str = ""
    ) -> tuple[bool, str]:
        if not username:
            return False, "用户名不能为空"
        if password and len(password) < 6:
            return False, "密码不能少于6位"
        if self.database.username_exists(username, exclude_id=account_id):
            return False, "用户名已存在"
        password_hash = self.password_hasher.hash(password) if password else None
        self.database.update_account(account_id, username, password_hash)
        return True, "修改成功"

    def change_password(
        self, username: str, old_password: str, new_password: str
    ) -> tuple[bool, str]:
        account = self.database.get_account_auth_data(username)
        if account is None or not self.password_hasher.verify(
            old_password, account["password"]
        ):
            return False, "原密码错误"
        if not new_password or len(new_password) < 6:
            return False, "新密码不能少于6位"
        self.database.update_password_hash(
            username, self.password_hasher.hash(new_password)
        )
        return True, "密码修改成功"

    def delete_account(self, account_id: int) -> tuple[bool, str]:
        account = self.database.get_account_by_id(account_id)
        if account is None:
            return False, "账号不存在"
        if account["username"] == "admin":
            return False, "admin 账号不可删除"
        if self.database.count_transactions_by_account(account["accountcode"]):
            return False, "该账号存在交易记录，无法删除"
        self.database.delete_account(account_id)
        return True, "删除成功"
