# This file is used to select the data from the table

from pydantic import BaseModel
from db.db import engine
from models.gem_models import Gem, GemProperties
from sqlmodel import Session,select


def select_all_gems():
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)       #Join is used to join two tables
       # statement = statement.where(Gem.id > 0).where(Gem.id < 2)
        #statement = statement.where(or_(Gem.id>1, Gem.price!=2000))
        result = session.exec(statement)
        res = []
        for gem, props in result:
            res.append({'gem': gem, 'props': props})
        return res
#select_all_gems() 

class GemPropertiesResponse(BaseModel):
    property_name: str
    property_value: str

class GemResponse(BaseModel):
    id: int
    name: str 
    properties: list[GemPropertiesResponse]
    class Config:
        orm_mode = True

def select_gem(id):
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)
        statement = statement.where(Gem.id == id)
        result = session.exec(statement).first()

        if result is None:
            return None
        
        gem, properties = result
        response = GemResponse(
            id=gem.id,
            name=gem.gem_type,
            properties=[
                GemPropertiesResponse(
                    property_name='size',
                    property_value=str(properties.size)
                ),
                GemPropertiesResponse(
                    property_name='clarity',
                    property_value=str(properties.clarity)
                ),
                GemPropertiesResponse(
                    property_name='color',
                    property_value=str(properties.color)
                )
            ]
        )
        return response
#select_gem(1)