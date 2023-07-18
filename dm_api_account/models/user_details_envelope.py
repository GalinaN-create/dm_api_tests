from pydantic import BaseModel, StrictInt, StrictStr, StrictBool, StrictInt, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Roles(Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator '


class Enum(Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class Rating(BaseModel):
    enabled: StrictBool
    quality: StrictInt
    quantity: StrictInt


class Info(BaseModel):
    value: StrictStr
    parse_mode: List[Enum] = Field(alias='parseMode')


# class EnumSetting(StrictStr):
#     MODERN = 'Modern'
#     PALE = 'Pale'
#     CLASSIC = 'Classic'
#     CLASSIC_PALE = 'ClassicPale'
#     NIGHT = 'Night'


class Paging(BaseModel):
    posts_per_page: StrictInt = Field(alias='postsPerPage')
    comments_per_page: StrictInt = Field(alias='commentsPerPage')
    topics_per_page: StrictInt = Field(alias='topicsPerPage')
    messages_per_page: StrictInt = Field(alias='messagesPerPage')
    entities_per_page: StrictInt = Field(alias='entitiesPerPage')


class Setting(BaseModel):
    color_schema: Optional[StrictStr] = Field(default=None, alias='colorSchema')
    nanny_greetings_message: StrictStr = Field(alias='nannyGreetingsMessage')
    paging: Paging


class Resource(BaseModel):
    login: StrictStr
    roles: Roles
    medium_picture_url: StrictStr = Field(alias='mediumPictureUrl')
    small_picture_url: StrictStr = Field(alias='smallPictureUrl')
    status: StrictStr
    rating: Rating
    online: datetime
    name: StrictStr
    location: StrictStr
    registration: datetime
    icq: StrictStr
    skype: StrictStr
    originalPictureUrl: StrictStr
    info: Info
    settings: Setting


class Metadata(BaseModel):
    email: StrictStr


class UserDetailsEnvelope(BaseModel):
    resource: Optional[Resource] = Field(default=None)
    metadata: Optional[Metadata] = Field(default=None)
