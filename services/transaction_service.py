from database import Database
from session import UserSession


class TransactionService:
    def __init__(self, database: Database, session: UserSession):
        self.database = database
        self.session = session

    def get_categories(self, type=None):
        return self.database.get_categories(type)

    def add_transaction(self, **data):
        return self.database.add_transaction(self.session.accountcode, **data)

    def update_transaction(self, transaction_id: int, **data):
        return self.database.update_transaction(
            self.session.accountcode, transaction_id, **data
        )

    def delete_transaction(self, transaction_id: int):
        return self.database.delete_transaction(
            self.session.accountcode, transaction_id
        )

    def get_transactions(self, **filters):
        return self.database.get_transactions(self.session.accountcode, **filters)

    def get_summary(self, start_date: str, end_date: str):
        return self.database.get_summary(
            self.session.accountcode, start_date, end_date
        )

    def get_monthly_summary(self, year: int, month: int):
        return self.database.get_monthly_summary(
            self.session.accountcode, year, month
        )

    def get_category_summary(
        self, start_date: str, end_date: str, type: str = "expense"
    ):
        return self.database.get_category_summary(
            self.session.accountcode, start_date, end_date, type
        )
