"""当前登录用户的内存会话状态。

会话只在程序运行期间保存账号编号和用户名，不持久化到数据库，也不保存密码。
AuthService 负责登录和退出时更新会话，其他 Service 通过注入的同一会话对象
读取当前账号信息。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserInfo:
    """不可变的当前用户信息。"""

    # 永久唯一账号编号，用于关联和隔离不同账号的交易数据。
    accountcode: int
    # 当前账号的登录用户名，主要用于界面展示和身份识别。
    username: str


class UserSession:
    """管理单次应用登录周期内的用户状态。"""

    def __init__(self):
        """创建未登录会话；None 表示当前没有登录用户。"""
        self._user: Optional[UserInfo] = None

    def login(self, accountcode: int, username: str):
        """保存认证成功后的用户信息，进入已登录状态。"""
        self._user = UserInfo(accountcode=accountcode, username=username)

    def logout(self):
        """清空当前用户，恢复未登录状态。"""
        self._user = None

    @property
    def is_logged_in(self) -> bool:
        """返回当前会话是否已有登录用户。"""
        return self._user is not None

    @property
    def user(self) -> UserInfo:
        """返回完整用户信息；未登录时抛出明确异常。"""
        if self._user is None:
            raise RuntimeError("当前用户未登录")
        return self._user

    @property
    def accountcode(self) -> int:
        """返回当前账号唯一编号，并复用 user 属性的未登录检查。"""
        return self.user.accountcode

    @property
    def username(self) -> str:
        """返回当前用户名，并复用 user 属性的未登录检查。"""
        return self.user.username
