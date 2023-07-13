from pydantic import BaseModel, StrictStr, Field
from enum import Enum
from typing import List

registration_model = {
    "login": "admin18",
    "email": "admin18@test.ru",
    "password": ["admin18"],
    "roles": ["manager", "user"]
}


class Roles(Enum):
    MANAGER = 'manager'
    USER = 'user'


class RegistrationModel(BaseModel.model_dump):
    login: StrictStr = Field(default='test')
    email: StrictStr = Field(alias='email', title='Email')
    password: StrictStr = List["password"]
    manager: StrictStr = Field(default="test")


print(RegistrationModel(**registration_model).json())
