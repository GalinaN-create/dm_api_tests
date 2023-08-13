from typing import List

import allure
from sqlalchemy import select, update
from generic.helpers.orm_models import User

from orm_client.orm_client import OrmClient


@allure.suite('Получение данных из БД')
@allure.title('Данные из БД')
class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        with allure.step('Получение всех пользователей из БД'):
            query = select([User])
            dataset = self.db.sent_query(query)
        return dataset

    def get_user_by_login(self, login) -> List[User]:
        with allure.step('Получение юзера по логину из БД'):
            query = select([User]).where(
                User.Login == login
            )
        dataset = self.db.sent_query(query)
        return dataset

    def delete_user_by_login(self, login):
        with allure.step('Удаление юзера по логину из БД'):
            query = User.__table__.delete().where(
                User.Login == login
            )
        self.db.sent_bulk_query(query)

    def activated_new_user(self, login):
        with allure.step('Активация нового пользователя через БД'):
            query = update(User).where(
                User.Login == login
            ).values(
                Activated=True
            )
        self.db.sent_bulk_query(query)
