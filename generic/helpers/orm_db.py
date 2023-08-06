from typing import List

from sqlalchemy import select, update, delete
from generic.helpers.orm_models import User

from orm_client.orm_client import OrmClient


class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        query = select([User])
        dataset = self.db.sent_query(query)
        return dataset

    def get_user_by_login(self, login) -> List[User]:
        query = select([User]).where(
            User.Login == login
        )
        dataset = self.db.sent_query(query)
        return dataset

    def delete_user_by_login(self, login):
        query = User.__table__.delete().where(
            User.Login == login
        )
        self.db.sent_bulk_query(query)

    def activated_new_user(self, login):
        query = update(User).where(
            User.Login == login
        ).values(
            Activated=True
        )
        self.db.sent_bulk_query(query)

