"""
__init__：初始化数据库对象
_get_sql_path：获取指定sql脚本的绝对路径
"""
import os
import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional
from session import UserSession


class Database:
    def __init__(self, session: UserSession, db_path: str = "account_book.db"):
        self.session = session
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
        self.conn.execute("PRAGMA foreign_keys = ON")

    def _get_sql_path(self, filename: str) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, 'sql', filename)

    def _create_tables(self):
        init_sql_path = self._get_sql_path('init.sql')
        with open(init_sql_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()
        self._init_default_account()
        self._init_default_categories()

    def _init_default_account(self):
        self.cursor.execute("SELECT COUNT(*) FROM my_account")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(
                "INSERT INTO my_account (accountcode, username, password) VALUES (?, ?, ?)",
                (1000000, 'admin', '123456')
            )
            self.conn.commit()

    def verify_account(self, username: str, password: str) -> bool:
        self.cursor.execute(
            "SELECT COUNT(*) FROM my_account WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone()[0] > 0

    def get_account_by_username(self, username: str) -> Optional[Dict]:
        row = self.conn.execute(
            "SELECT id, accountcode, username FROM my_account WHERE username = ?",
            (username,)
        ).fetchone()
        return dict(row) if row else None

    def _require_current_accountcode(self) -> int:
        return self.session.accountcode

    def change_password(self, username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        if not self.verify_account(username, old_password):
            return False, "原密码错误"
        if not new_password or len(new_password) < 6:
            return False, "新密码不能少于6位"
        self.cursor.execute(
            "UPDATE my_account SET password = ?, updateTime = CURRENT_TIMESTAMP WHERE username = ?",
            (new_password, username)
        )
        self.conn.commit()
        return True, "密码修改成功"

    def get_accounts(self) -> List[Dict]:
        self.cursor.execute("SELECT * FROM my_account ORDER BY createTime DESC")
        return [dict(row) for row in self.cursor.fetchall()]

    def add_account(self, username: str, password: str) -> tuple[bool, str]:
        if not username:
            return False, "用户名不能为空"
        if not password or len(password) < 6:
            return False, "密码不能少于6位"
        self.cursor.execute("SELECT COUNT(*) FROM my_account WHERE username = ?", (username,))
        if self.cursor.fetchone()[0] > 0:
            return False, "用户名已存在"
        next_code = self.conn.execute(
            "SELECT COALESCE(MAX(accountcode), 999999) + 1 FROM my_account"
        ).fetchone()[0]
        self.cursor.execute(
            "INSERT INTO my_account (accountcode, username, password) VALUES (?, ?, ?)",
            (next_code, username, password)
        )
        self.conn.commit()
        return True, "添加成功"

    def update_account(self, id: int, username: str, password: str) -> tuple[bool, str]:
        if not username:
            return False, "用户名不能为空"
        if not password or len(password) < 6:
            return False, "密码不能少于6位"
        self.cursor.execute(
            "SELECT COUNT(*) FROM my_account WHERE username = ? AND id != ?",
            (username, id)
        )
        if self.cursor.fetchone()[0] > 0:
            return False, "用户名已存在"
        self.cursor.execute(
            "UPDATE my_account SET username = ?, password = ?, updateTime = CURRENT_TIMESTAMP WHERE id = ?",
            (username, password, id)
        )
        self.conn.commit()
        return True, "修改成功"

    def delete_account(self, id: int) -> tuple[bool, str]:
        self.cursor.execute(
            "SELECT username, accountcode FROM my_account WHERE id = ?", (id,)
        )
        row = self.cursor.fetchone()
        if row is None:
            return False, "账号不存在"
        if row[0] == 'admin':
            return False, "admin 账号不可删除"
        transaction_count = self.conn.execute(
            "SELECT COUNT(*) FROM my_transactions WHERE accountcode = ?",
            (row['accountcode'],)
        ).fetchone()[0]
        if transaction_count:
            return False, "该账号存在交易记录，无法删除"
        self.cursor.execute(
            "DELETE FROM my_account WHERE id = ?", (id,)
        )
        self.conn.commit()
        return True, "删除成功"

    def _init_default_categories(self):
        self.cursor.execute("SELECT COUNT(*) FROM my_categories")
        if self.cursor.fetchone()[0] == 0:
            default_categories = [
                ('餐饮', 'expense', '🍔'),
                ('交通', 'expense', '🚗'),
                ('购物', 'expense', '🛒'),
                ('娱乐', 'expense', '🎮'),
                ('居住', 'expense', '🏠'),
                ('医疗', 'expense', '💊'),
                ('教育', 'expense', '📚'),
                ('其他支出', 'expense', '📦'),
                ('工资', 'income', '💰'),
                ('奖金', 'income', '💵'),
                ('投资', 'income', '📈'),
                ('其他收入', 'income', '💎'),
            ]
            self.cursor.executemany(
                "INSERT INTO my_categories (name, type, icon) VALUES (?, ?, ?)",
                default_categories
            )
            self.conn.commit()

    def get_categories(self, type: Optional[str] = None) -> List[Dict]:
        if type:
            self.cursor.execute(
                "SELECT * FROM my_categories WHERE type = ? ORDER BY id", (type,)
            )
        else:
            self.cursor.execute("SELECT * FROM my_categories ORDER BY id")
        return [dict(row) for row in self.cursor.fetchall()]

    def add_category(self, name: str, type: str, icon: str = '📁') -> int:
        self.cursor.execute(
            "INSERT INTO my_categories (name, type, icon) VALUES (?, ?, ?)",
            (name, type, icon)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_category(self, category_id: int):
        self.cursor.execute("DELETE FROM my_categories WHERE id = ?", (category_id,))
        self.conn.commit()

    def add_transaction(self, type: str, amount: float, category_id: int,
                       note: str, date: str) -> int:
        accountcode = self._require_current_accountcode()
        self.cursor.execute(
            """INSERT INTO my_transactions
               (accountcode, type, amount, category_id, note, date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (accountcode, type, amount, category_id, note, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_transaction(self, id: int, type: str, amount: float,
                           category_id: int, note: str, date: str):
        accountcode = self._require_current_accountcode()
        self.cursor.execute(
            """UPDATE my_transactions SET type=?, amount=?, category_id=?, note=?, date=?, updateTime=CURRENT_TIMESTAMP
               WHERE id=? AND accountcode=?""",
            (type, amount, category_id, note, date, id, accountcode)
        )
        self.conn.commit()

    def delete_transaction(self, id: int):
        accountcode = self._require_current_accountcode()
        self.cursor.execute(
            "DELETE FROM my_transactions WHERE id = ? AND accountcode = ?",
            (id, accountcode)
        )
        self.conn.commit()

    def get_transactions(self, start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         type: Optional[str] = None,
                         category_id: Optional[int] = None) -> List[Dict]:
        accountcode = self._require_current_accountcode()
        query = """
            SELECT t.*, c.name as category_name, c.icon as category_icon
            FROM my_transactions t
            LEFT JOIN my_categories c ON t.category_id = c.id
            WHERE t.accountcode = ?
        """
        params = [accountcode]

        if start_date:
            query += " AND t.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND t.date <= ?"
            params.append(end_date)
        if type:
            query += " AND t.type = ?"
            params.append(type)
        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)

        query += " ORDER BY t.date DESC, t.createTime DESC"
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_summary(self, start_date: str, end_date: str) -> Dict:
        accountcode = self._require_current_accountcode()
        self.cursor.execute(
            """SELECT
                COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as total_income,
                COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as total_expense
            FROM my_transactions
            WHERE accountcode = ? AND date >= ? AND date < ?""",
            (accountcode, start_date, end_date)
        )
        row = dict(self.cursor.fetchone())
        row['balance'] = row['total_income'] - row['total_expense']
        return row

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        accountcode = self._require_current_accountcode()
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month+1:02d}-01"

        self.cursor.execute(
            """SELECT
                COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as total_income,
                COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as total_expense
            FROM my_transactions
            WHERE accountcode = ? AND date >= ? AND date < ?""",
            (accountcode, start_date, end_date)
        )
        row = dict(self.cursor.fetchone())
        row['balance'] = row['total_income'] - row['total_expense']
        return row

    def get_category_summary(self, start_date: str, end_date: str, type: str = 'expense') -> List[Dict]:
        accountcode = self._require_current_accountcode()
        self.cursor.execute(
            """SELECT COALESCE(c.name, '未分类') AS name,
                      COALESCE(c.icon, '📁') AS icon,
                      SUM(t.amount) AS total
            FROM my_transactions t
            LEFT JOIN my_categories c ON t.category_id = c.id
            WHERE t.accountcode = ? AND t.date >= ? AND t.date < ? AND t.type = ?
            GROUP BY t.category_id
            ORDER BY total DESC""",
            (accountcode, start_date, end_date, type)
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        self.conn.close()
