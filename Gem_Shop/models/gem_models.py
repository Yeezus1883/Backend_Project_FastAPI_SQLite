from typing import Optional
from sqlmodel import Relationship, SQLModel,Field             #Field is also an instance of SQLModel
from enum import Enum as Enum_, IntEnum
from models.user_models import User

class Enum(Enum_):
    @classmethod                    #classmethod is a decorator which is used to define a method which is bound to the class and not the object of the class
    def list(cls):
        return list(map(lambda c: c.value, cls))              #lambda is a function which is used to create an anonymous function, it is used to create a function which is not defined by a name


class GemClarity(IntEnum):
    SI=1
    VS=2
    VVS=3
    IF=4
    FL=5


class GemType(str,Enum):
    Diamond='Diamond'
    Ruby='Ruby'
    Sapphire='Sapphire'
    Emerald='Emerald'



class GemColor(str,Enum):       #Enum is a class in python which is used to create enumerations, which are a set of symbolic names (members) bound to unique, constant values.
    D='D'
    F='F' 
    E='E'
    H='H'
    G='G'
    I='I'


class GemProperties(SQLModel,table=True):                               #Inheriting from SQLModel
    id: Optional[int]= Field(primary_key=True)                          #Field(primary_key=True)
    size: float=1
    clarity: Optional[GemClarity]=None                                  #Optional is used to make the field optional and is imported from typing
    color:Optional[GemColor]=None
    gem:Optional['Gem']=Relationship(back_populates='gem_properties')   #We put 'Gem' in quotes because it is not defined yet, it is defined below
    



class Gem(SQLModel, table=True): # Inheriting from SQLModel
    id: Optional[int]= Field(primary_key=True)                      #Declare primary key as optional because it will be auto generated 
    price:float
    available:bool=True
    gem_type:GemType=GemType.Diamond
    gem_properties_id: Optional[int]=Field(default=None,foreign_key='gemproperties.id') #foreign_key is used to create a foreign key constraint, Here gemproperties is the table name and id is the column name
    gem_properties:Optional[GemProperties]=Relationship(back_populates='gem') #Relationship is used to create a relationship between two tables, back_populates is used to specify the column name in the other table
    seller_id:Optional[int]=Field(default=None,foreign_key='user.id')
    seller:Optional[User]=Relationship() 


class GemPatch(SQLModel): 
    id: Optional[int]= Field(primary_key=True)                      #Declare primary key as optional because it will be auto generated 
    price:Optional[float]=1000
    available:Optional[bool]=True
    gem_type:Optional[GemType]=GemType.Diamond

    gem_properties_id: Optional[int]=Field(default=None,foreign_key='gemproperties.id') #foreign_key is used to create a foreign key constraint, Here gemproperties is the table name and id is the column name
    gem_properties:Optional[GemProperties]=Relationship(back_populates='gem') #Relationship is used to create a relationship between two tables, back_populates is used to specify the column name in the other table
