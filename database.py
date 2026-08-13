"""SQLite 数据访问层。

本模块只负责表初始化和 SQL 读写，不处理登录会话、密码哈希或业务校验。
账号、认证和交易业务规则分别由 services 包中的 Service 负责。
"""
import os
import sqlite3
from typing import List, Dict, Optional


class Database:
    """提供账号、分类、交易记录和记事本的底层持久化接口。"""

    def __init__(self, db_path: str = "account_book.db"):
        """连接 SQLite 数据库并初始化表结构及默认分类。"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
        self.conn.execute("PRAGMA foreign_keys = ON")

    def _get_sql_path(self, filename: str) -> str:
        """返回 sql 目录中指定脚本的绝对路径。"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, 'sql', filename)

    def _create_tables(self):
        """执行初始化 SQL，并在分类表为空时写入默认分类。"""
        init_sql_path = self._get_sql_path('init.sql')
        with open(init_sql_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()
        self._init_default_categories()

    def get_account_auth_data(self, username: str) -> Optional[Dict]:
        """查询认证所需账号信息，包含密码哈希，仅供认证服务使用。"""
        row = self.conn.execute(
            """SELECT id, accountcode, username, password
               FROM my_account WHERE username = ?""",
            (username,)
        ).fetchone()
        return dict(row) if row else None

    def update_password_hash(self, username: str, password_hash: str):
        """更新指定账号的密码哈希和更新时间。"""
        with self.conn:
            self.conn.execute(
                """UPDATE my_account
                   SET password = ?, updateTime = datetime('now', '+8 hours')
                   WHERE username = ?""",
                (password_hash, username)
            )

    def get_accounts(self) -> List[Dict]:
        """返回账号列表，不包含密码哈希。"""
        self.cursor.execute(
            """SELECT id, accountcode, username, createTime, updateTime
               FROM my_account ORDER BY createTime DESC"""
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def username_exists(self, username: str, exclude_id: int | None = None) -> bool:
        """检查用户名是否存在；exclude_id 用于编辑账号时排除自身。"""
        if exclude_id is None:
            row = self.conn.execute(
                "SELECT 1 FROM my_account WHERE username = ?", (username,)
            ).fetchone()
        else:
            row = self.conn.execute(
                "SELECT 1 FROM my_account WHERE username = ? AND id != ?",
                (username, exclude_id)
            ).fetchone()
        return row is not None

    def get_next_accountcode(self) -> int:
        """生成下一个账号编号，初始编号为 1000000。"""
        return self.conn.execute(
            "SELECT COALESCE(MAX(accountcode), 999999) + 1 FROM my_account"
        ).fetchone()[0]

    def insert_account(self, accountcode: int, username: str, password_hash: str):
        """插入账号；password_hash 必须是安全组件生成的密码哈希。"""
        with self.conn:
            self.conn.execute(
                """INSERT INTO my_account (accountcode, username, password)
                   VALUES (?, ?, ?)""",
                (accountcode, username, password_hash)
            )

    def update_account(
        self, account_id: int, username: str, password_hash: str | None = None
    ):
        """更新用户名，并在提供 password_hash 时同时更新密码。"""
        with self.conn:
            if password_hash is not None:
                self.conn.execute(
                    """UPDATE my_account
                       SET username = ?, password = ?,
                           updateTime = datetime('now', '+8 hours')
                       WHERE id = ?""",
                    (username, password_hash, account_id)
                )
            else:
                self.conn.execute(
                    """UPDATE my_account
                       SET username = ?,
                           updateTime = datetime('now', '+8 hours')
                       WHERE id = ?""",
                    (username, account_id)
                )

    def get_account_by_id(self, account_id: int) -> Optional[Dict]:
        """按主键查询不含密码的账号信息。"""
        row = self.conn.execute(
            "SELECT id, accountcode, username FROM my_account WHERE id = ?",
            (account_id,)
        ).fetchone()
        return dict(row) if row else None

    def count_transactions_by_account(self, accountcode: int) -> int:
        """统计指定账号拥有的交易记录数量。"""
        return self.conn.execute(
            "SELECT COUNT(*) FROM my_transactions WHERE accountcode = ?",
            (accountcode,)
        ).fetchone()[0]

    def count_notebooks_by_account(self, accountcode: int) -> int:
        """统计指定账号拥有的记事本数量。"""
        return self.conn.execute(
            "SELECT COUNT(*) FROM my_notebooks WHERE accountcode = ?",
            (accountcode,)
        ).fetchone()[0]

    def delete_account(self, account_id: int):
        """按主键删除账号；是否允许删除由 AccountService 判断。"""
        with self.conn:
            self.conn.execute("DELETE FROM my_account WHERE id = ?", (account_id,))

    def _init_default_categories(self):
        """分类表为空时写入系统默认收入和支出分类。"""
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
                """INSERT INTO my_categories (name, type, icon)
                   VALUES (?, ?, ?)""",
                default_categories
            )
            self.conn.commit()

    def get_categories(self, type: Optional[str] = None) -> List[Dict]:
        """返回分类列表；type 可为 income、expense 或 None。"""
        if type:
            self.cursor.execute(
                "SELECT * FROM my_categories WHERE type = ? ORDER BY id", (type,)
            )
        else:
            self.cursor.execute("SELECT * FROM my_categories ORDER BY id")
        return [dict(row) for row in self.cursor.fetchall()]

    def add_notebook(self, accountcode: int, title: str, content: str) -> int:
        """为指定账号新增记事本，并返回记事本主键。"""
        with self.conn:
            cursor = self.conn.execute(
                """INSERT INTO my_notebooks (accountcode, title, content)
                   VALUES (?, ?, ?)""",
                (accountcode, title, content),
            )
        return cursor.lastrowid

    def update_notebook(
        self, accountcode: int, notebook_id: int, title: str, content: str
    ) -> bool:
        """更新指定账号的记事本，返回是否找到并更新记录。"""
        with self.conn:
            cursor = self.conn.execute(
                """UPDATE my_notebooks
                   SET title = ?, content = ?,
                       updateTime = datetime('now', '+8 hours')
                   WHERE id = ? AND accountcode = ?""",
                (title, content, notebook_id, accountcode),
            )
        return cursor.rowcount > 0

    def get_notebook(self, accountcode: int, notebook_id: int) -> Optional[Dict]:
        """按账号和主键查询单个记事本。"""
        row = self.conn.execute(
            """SELECT id, accountcode, title, content, createTime, updateTime
               FROM my_notebooks WHERE id = ? AND accountcode = ?""",
            (notebook_id, accountcode),
        ).fetchone()
        return dict(row) if row else None

    def get_notebooks(self, accountcode: int, keyword: str = "") -> List[Dict]:
        """按创建日期分组、组内更新时间倒序查询指定账号的记事本。"""
        query = """SELECT id, accountcode, title, content, createTime, updateTime
                   FROM my_notebooks WHERE accountcode = ?"""
        params = [accountcode]
        if keyword:
            query += " AND (title LIKE ? OR content LIKE ?)"
            pattern = f"%{keyword}%"
            params.extend((pattern, pattern))
        query += """ ORDER BY date(createTime) DESC,
                     updateTime DESC, id DESC"""
        rows = self.conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def add_transaction(self, accountcode: int, type: str, amount: float, category_id: int,
                       note: str, date: str) -> int:
        """为指定账号新增交易，并返回交易主键。"""
        self.cursor.execute(
            """INSERT INTO my_transactions
               (accountcode, type, amount, category_id, note, date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (accountcode, type, amount, category_id, note, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_transaction(self, accountcode: int, id: int, type: str, amount: float,
                           category_id: int, note: str, date: str):
        """更新指定账号的交易，账号编号用于限制数据访问范围。"""
        self.cursor.execute(
            """UPDATE my_transactions
               SET type=?, amount=?, category_id=?, note=?, date=?,
                   updateTime=datetime('now', '+8 hours')
               WHERE id=? AND accountcode=?""",
            (type, amount, category_id, note, date, id, accountcode)
        )
        self.conn.commit()

    def delete_transaction(self, accountcode: int, id: int):
        """删除指定账号的交易，避免跨账号删除。"""
        self.cursor.execute(
            "DELETE FROM my_transactions WHERE id = ? AND accountcode = ?",
            (id, accountcode)
        )
        self.conn.commit()

    def get_transactions(self, accountcode: int, start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         type: Optional[str] = None,
                         category_id: Optional[int] = None) -> List[Dict]:
        """按账号及可选条件查询交易。

        start_date 和 end_date 均为包含边界，格式为 YYYY-MM-DD。
        """
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

    def get_summary(self, accountcode: int, start_date: str, end_date: str) -> Dict:
        """汇总指定账号的收入、支出和结余。

        日期区间采用左闭右开规则：[start_date, end_date)。
        """
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

    def get_monthly_summary(self, accountcode: int, year: int, month: int) -> Dict:
        """返回指定账号某月的收入、支出和结余。"""
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

    def get_category_summary(self, accountcode: int, start_date: str, end_date: str, type: str = 'expense') -> List[Dict]:
        """按分类汇总指定账号的收入或支出。

        日期区间采用左闭右开规则：[start_date, end_date)。
        """
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
        """关闭 SQLite 连接，连接生命周期由应用入口统一管理。"""
        self.conn.close()
