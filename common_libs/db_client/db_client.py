import json
import uuid

import allure
import records
import requests
import structlog


def allure_attach_db(fn):
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if query:
            allure.attach(
                query,
                name='db_request',
                attachment_type=allure.attachment_type.TEXT
            )
        response = fn(*args, **kwargs)
        try:
            dataset = response.as_dict()
        except AttributeError:
            return response
        allure.attach(
            json.dumps(dataset, indent=2),
            name='db_response',
            attachment_type=allure.attachment_type.JSON
        )
        return response
    return wrapper


class DbClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        self.db = records.Database(connection_string, isolation_level=isolation_level)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service="db")

# Метод для выполнения sql запроса к бд
    @allure_attach_db
    def sent_query(self, query):
    # Печать переданного запроса
        print(query)
    # Создание логгера с уникальным айди события
        log = self.log.bind(event_id=str(uuid.uuid4()))
    # Записывается информация в логгер о событии реквест с переданным запросом
        log.msg(
            event='request',
            query=query
        )
    # Выполняется sql запрос с использованием обьекта self.db и результат представляется в виде словаря датасет
        dataset = self.db.query(query=query).as_dict()
    # В логгере записывается информация о событии респонс с полученным набором данных датасет
        log.msg(
            event='response',
            dataset=dataset
        )
    # Возвращается полученный датасет
        return dataset

    @allure_attach_db
    def sent_bulk_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        self.db.bulk_query(query=query)
