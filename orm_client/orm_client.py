import json
import uuid

import allure
import records
import requests
import structlog
from sqlalchemy import create_engine


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        body = kwargs.get('str')
        if body:
            allure.attach(
                json.dumps(kwargs.get('str'), indent=2),
                name='request',
                attachment_type=allure.attachment_type.__str__()
            )
        response = fn(*args, **kwargs)
        return response
    return wrapper


class OrmClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        print(connection_string)
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(self.__class__.__name__).bind(service="db")

    def close_connection(self):
        self.db.close()

    @allure_attach
    def sent_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        dataset = self.db.execute(statement=query)
        result = [row for row in dataset]
        log.msg(
            event='response',
            dataset=[dict(row) for row in result]
        )
        return result
        print(result)

    @allure_attach
    def sent_bulk_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        self.db.execute(statement=query)
