from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserInfo:
    accountcode: int
    username: str


class UserSession:
    def __init__(self):
        self._user: Optional[UserInfo] = None

    def login(self, accountcode: int, username: str):
        self._user = UserInfo(accountcode=accountcode, username=username)

    def logout(self):
        self._user = None

    @property
    def is_logged_in(self) -> bool:
        return self._user is not None

    @property
    def user(self) -> UserInfo:
        if self._user is None:
            raise RuntimeError("当前用户未登录")
        return self._user

    @property
    def accountcode(self) -> int:
        return self.user.accountcode

    @property
    def username(self) -> str:
        return self.user.username
