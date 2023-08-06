import time
import pytest

from generic.helpers.mailhog import MailhogApi

from dm_api_account.models.registration_model import Registration
from dm_api_account.models.login_credentials_model import LoginCredentials

import requests
from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from dm_api_account.models.reset_password_model import ResetPassword

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host="http://localhost:5025")


@pytest.fixture
def dm_api_facade(mailhog):
    return Facade(host="http://localhost:5051", mailhog=mailhog)


@pytest.fixture
def orm_db():
    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')
    return orm
