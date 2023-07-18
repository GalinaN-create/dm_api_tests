# from pydantic import BaseModel, StrictStr, Field
# from typing import Optional
#
#
# class InvalidProperties(BaseModel):
#     additional_prop_1: StrictStr = Field(alias='additionalProp1')
#     additional_prop_2: StrictStr = Field(alias='additionalProp2')
#     additional_prop_3: StrictStr = Field(alias='additionalProp3')
#
#
# class BadRequestError(BaseModel):
#     # message: Optional[StrictStr] = Field(default=None)
#     invalid_properties: Optional[InvalidProperties] = Field(default=None, alias='invalidProperties')
