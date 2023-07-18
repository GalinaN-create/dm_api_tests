from pydantic import BaseModel, StrictStr, UUID4, Field
from typing import Optional


class ChangePassword(BaseModel):
    login: Optional[StrictStr] = Field(default=None)
    token: Optional[UUID4] = Field(default=None)
    oldPassword: Optional[StrictStr] = Field(default=None)
    newPassword: Optional[StrictStr] = Field(default=None)

