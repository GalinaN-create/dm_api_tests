from pydantic import BaseModel, StrictStr, Field
from typing import Optional


class ResetPassword(BaseModel):
    login: Optional[StrictStr] = Field(default=None)
    email: Optional[StrictStr] = Field(default=None)
