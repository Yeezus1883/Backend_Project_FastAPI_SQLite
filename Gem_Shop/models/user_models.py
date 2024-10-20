import datetime
from typing import Optional
from sqlmodel import Relationship, SQLModel,Field             #Field is also an instance of SQLModel
from pydantic import EmailStr, field_validator,validator

class User(SQLModel,table=True):
    id: Optional[int]= Field(primary_key=True)                          #Field(primary_key=True)
    username:str=Field(index=True)
    password:str=Field(max_length=100,min_length=8)         #Field is used to specify the constraints on the field
    email:EmailStr
    created_at:datetime.datetime=datetime.datetime.now()
    is_seller:bool=False


class UserInput(SQLModel):
    username:str
    password:str=Field(max_length=100,min_length=8)  
    password2:str
    email:EmailStr
    is_seller:bool=False

    @validator('password2')
    def password_match(cls,v,values,**kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
class UserLogin(SQLModel):
    username:str
    password:str