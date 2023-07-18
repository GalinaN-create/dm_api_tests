# from __future__ import annotations
#
# from datetime import datetime
# from enum import Enum
# from typing import Any, Dict, List, Optional
# from uuid import UUID
#
# from pydantic import BaseModel, Extra, Field, StrictStr
#
#
# class BadRequestError(BaseModel):
#     class Config:
#         extra = Extra.forbid
#
#     message: Optional[StrictStr] = Field(None, description='Client message')
#     invalid_properties: Optional[Dict[str, List[StrictStr]]] = Field(
#         None,
#         alias='invalidProperties',
#         description='Key-value pairs of invalid request properties',
#     )
