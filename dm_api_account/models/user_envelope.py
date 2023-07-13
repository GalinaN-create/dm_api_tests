from pydantic import BaseModel, StrictStr, StrictBool, Field, FutureDate
from enum import Enum
from typing import List, Optional


class Roles(Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class Rating:
    enabled: StrictBool
    quality: int
    quantity: int


class User(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(alias="mediumPictureUrl")
    small_picture_url: Optional[StrictStr] = Field(alias="smallPictureUrl")
    status: StrictStr
    rating: Rating
    online: FutureDate
    name: StrictStr
    location: StrictStr
    registration: FutureDate


class UserEnvelopeModel:
    resource: User
    metadata: StrictStr
