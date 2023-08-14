import allure

from db_client.db_client import DbClient


@allure.suite('Получение данных из БД')
class DmDatabase:
    def __init__(self, user, password, host, database):
        self.db = DbClient(user, password, host, database)

    def get_all_users(self):
        with allure.step('Получение всех юзеров из бд'):
            query = 'select * from "public"."Users"'
            dataset = self.db.sent_query(query=query)
        return dataset

    def get_user_by_login(self, login):
        with allure.step('Получение юзера по логину из бд'):
            query = f'''
            select * from "public"."Users"
            where "Login" = '{login}'
            '''
            dataset = self.db.sent_query(query=query)
        return dataset

    def delete_user_by_login(self, login):
        with allure.step('Удаление юзера по логину из бд'):
            query = f'''
            delete from "public"."Users" 
            where "Login" = '{login}'
            '''
            dataset = self.db.sent_bulk_query(query=query)
        return dataset

    def activated_new_user(self, login):
        with allure.step('Активация юзера через бд'):
            query = f'''
            update "public"."Users"
            set "Activated" = True
            where "Login" = '{login}'
            '''
            dataset = self.db.sent_bulk_query(query=query)
        return dataset
