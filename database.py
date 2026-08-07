import os
import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_path: str = "account_book.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _get_sql_path(self, filename: str) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, 'sql', filename)

    def _create_tables(self):
        init_sql_path = self._get_sql_path('init.sql')
        with open(init_sql_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()
        self._init_default_categories()

    def _init_default_categories(self):
        self.cursor.execute("SELECT COUNT(*) FROM categories")
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
                "INSERT INTO categories (name, type, icon) VALUES (?, ?, ?)",
                default_categories
            )
            self.conn.commit()

    def get_categories(self, type: Optional[str] = None) -> List[Dict]:
        if type:
            self.cursor.execute(
                "SELECT * FROM categories WHERE type = ? ORDER BY id", (type,)
            )
        else:
            self.cursor.execute("SELECT * FROM categories ORDER BY id")
        return [dict(row) for row in self.cursor.fetchall()]

    def add_category(self, name: str, type: str, icon: str = '📁') -> int:
        self.cursor.execute(
            "INSERT INTO categories (name, type, icon) VALUES (?, ?, ?)",
            (name, type, icon)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_category(self, category_id: int):
        self.cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()

    def add_transaction(self, type: str, amount: float, category_id: int,
                       note: str, date: str) -> int:
        self.cursor.execute(
            """INSERT INTO transactions (type, amount, category_id, note, date)
               VALUES (?, ?, ?, ?, ?)""",
            (type, amount, category_id, note, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_transaction(self, id: int, type: str, amount: float,
                          category_id: int, note: str, date: str):
        self.cursor.execute(
            """UPDATE transactions SET type=?, amount=?, category_id=?, note=?, date=?
               WHERE id=?""",
            (type, amount, category_id, note, date, id)
        )
        self.conn.commit()

    def delete_transaction(self, id: int):
        self.cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))
        self.conn.commit()

    def get_transactions(self, start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        type: Optional[str] = None,
                        category_id: Optional[int] = None) -> List[Dict]:
        query = """
            SELECT t.*, c.name as category_name, c.icon as category_icon
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params = []

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

        query += " ORDER BY t.date DESC, t.created_at DESC"
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_summary(self, start_date: str, end_date: str) -> Dict:
        self.cursor.execute(
            """SELECT
                COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as total_income,
                COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as total_expense
            FROM transactions
            WHERE date >= ? AND date <= ?""",
            (start_date, end_date)
        )
        row = dict(self.cursor.fetchone())
        row['balance'] = row['total_income'] - row['total_expense']
        return row

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month+1:02d}-01"

        self.cursor.execute(
            """SELECT
                COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as total_income,
                COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as total_expense
            FROM transactions
            WHERE date >= ? AND date < ?""",
            (start_date, end_date)
        )
        row = dict(self.cursor.fetchone())
        row['balance'] = row['total_income'] - row['total_expense']
        return row

    def get_category_summary(self, start_date: str, end_date: str, type: str = 'expense') -> List[Dict]:
        self.cursor.execute(
            """SELECT c.name, c.icon, SUM(t.amount) as total
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.date >= ? AND t.date <= ? AND t.type = ?
            GROUP BY t.category_id
            ORDER BY total DESC""",
            (start_date, end_date, type)
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        self.conn.close()
