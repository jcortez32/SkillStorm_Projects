from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, text

class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int 
    symbol:str
    name:str
    sector:str

class CreateCompanyDTO(BaseModel):
    # FORBIDDING any extra values being passed in to the object
    #   extra properties are typically just ignored, but with extra="forbid" you get ValidationError
    model_config = ConfigDict(extra="forbid")
    symbol:str
    name:str
    sector:str


    