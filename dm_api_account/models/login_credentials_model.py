from pydantic import BaseModel, StrictStr, StrictBool, Field
from typing import Optional


class LoginCredentials(BaseModel):
    login: Optional[StrictStr] = Field(default=None)
    password: Optional[StrictStr] = Field(default=None)
    rememberMe: Optional[StrictBool] = Field(default=None)
