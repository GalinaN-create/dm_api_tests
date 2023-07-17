from pydantic import BaseModel, StrictStr, StrictBool, Field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class Roles(Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class Rating(BaseModel):
    enabled: StrictBool
    quality: int
    quantity: int


class User(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(alias="mediumPictureUrl", default=None)
    small_picture_url: Optional[StrictStr] = Field(alias="smallPictureUrl", default=None)
    status: Optional[StrictStr] = Field(default=None)
    rating: Rating
    online: Optional[datetime] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    location: Optional[StrictStr] = Field(default=None)
    registration: Optional[datetime] = Field(default=None)


class UserEnvelopeModel(BaseModel):
    resource: User
    metadata: Optional[StrictStr] = Field(default=None)
