from database import Database
from security import PasswordHasher
from session import UserSession


class AuthService:
    def __init__(
        self,
        database: Database,
        password_hasher: PasswordHasher,
        session: UserSession,
    ):
        self.database = database
        self.password_hasher = password_hasher
        self.session = session

    def login(self, username: str, password: str) -> bool:
        account = self.database.get_account_auth_data(username)
        if account is None or not self.password_hasher.verify(
            password, account["password"]
        ):
            return False
        self.session.login(account["accountcode"], account["username"])
        return True

    def logout(self):
        self.session.logout()
