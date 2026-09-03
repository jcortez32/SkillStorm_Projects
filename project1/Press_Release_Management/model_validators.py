from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, text
from datetime import datetime
class Press(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int 
    headline:str
    body_test:str
    published_date:datetime
    company_id:int


class CreatePressDTO(BaseModel):
    # FORBIDDING any extra values being passed in to the object
    #   extra properties are typically just ignored, but with extra="forbid" you get ValidationError
    model_config = ConfigDict(extra="forbid")
    headline:str = Field(min_length=10) 
    body_test:str   #need to enforce max 5000 char
    published_date:str

class UpdatePressDTO(BaseModel):
    # FORBIDDING any extra values being passed in to the object
    #   extra properties are typically just ignored, but with extra="forbid" you get ValidationError
    model_config = ConfigDict(extra="forbid")
    headline:str | None = None
    body_test:str | None = None
    published_date:str | None = None # Note to self - Need to validate date as datetime instead of string (json only accepts string)


    