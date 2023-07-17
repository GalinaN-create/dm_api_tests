from pydantic import BaseModel, StrictStr, Field
from typing import Optional


class RegistrationModel(BaseModel):
    login: Optional[StrictStr] = Field(default=None)
    email: Optional[StrictStr] = Field(default=None)
    password: Optional[StrictStr] = Field(default=None)




