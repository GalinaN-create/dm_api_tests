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
    def post(self, path: str, **kwargs) -> Response:
        return self._send_request('POST', path, **kwargs)

    def get(self, path: str, **kwargs) -> Response:
        return self._send_request('GET', path, **kwargs)

    def put(self, path: str, **kwargs) -> Response:
        return self._send_request('PUT', path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self._send_request('DELETE', path, **kwargs)

    # Метод принимает запрос, оборачивает его в лог и после этого отдаёт обёрнутый запрос
    def _send_request(self, method, path, **kwargs):
        full_url = self.host + path
        log = self.log.bind(event_id=str(uuid.uuid4()))
        # Формируем лог - те необх данные, которые нам нужны
        # Параметры, которые увилдим до отправки
        log.msg(
            event='request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )
        # формируем запрос с нашими переменными, Куда будут возвращаться результаты нашего запроса
        response = self.session.request(
            method=method,
            url=full_url,
            **kwargs
        )
        # Формирование curl по запросу
        curl = curlify.to_curl(response.request)
        print(curl)
        # Подробный ответ (запуск курла)
        log.msg(
            event='response',
            status_code=response.status_code,
            headers=response.headers,
            json=self.get_json(response),
            text=response.text,
            content=response.content,
            curl=curl

        )
        return response
    @staticmethod
    def get_json(response):
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return

