from generic.helpers.orm_db import OrmDatabase


class AssertionsPostV1Account:

    def __init__(self, orm: OrmDatabase):
        self.orm = orm

    def check_user_was_created(self, login):
        dataset = self.orm.get_user_by_login(login=login)
        for row in dataset:
            assert row.Login == login, f'User {login} registered'
            assert row.Activated is False, f'User {login} was not activated'

    def check_user_was_activated(self, login):
        dataset = self.orm.get_user_by_login(login=login)
        for row in dataset:
            assert row.Activated is True, f'User {login} not activated'