import requests
from requests import session, Response
import structlog
import uuid
import curlify

class Restclient:

    def __init__(self, host, headers=None):
        self.host = host
        self.session = session()
        if headers:
            self.session.headers.update(headers)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='api')

    # Обёртка над rest методами
    def post(self, path: str, **kwargs):
        return self._send_request('POST', path, **kwargs)
    # Метод принимает запрос, оборачивает его в лог и после этого отдаёт обёрнутый запрос
    def _send_request(self, method, path, **kwargs):
        full_url = self.host + path
        log = self.log.bind(event_id=str(uuid.uuid4()))
        # Формируем лог - те необх данные, которые нам нужны
        log.msg(
            event='request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get(),
            json=kwargs.get(),
            data=kwargs.get('data')
        )
        response = self.session.request(
            method=method,
            url=full_url,
            **kwargs
        )
        curl = curlify.to_curl(response.request)
        print(curl)
        # Подробный ответ
