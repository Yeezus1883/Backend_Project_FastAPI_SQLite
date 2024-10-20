from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select
from starlette.status import HTTP_204_NO_CONTENT
from starlette.status import HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED
from fastapi.encoders import jsonable_encoder
from models.gem_models import *
from repos import gem_repository
from populate import calculate_gem_price
from db.db import session
from auth.auth import AuthHandler
auth_handler=AuthHandler()
from fastapi import HTTPException
from typing import List,Dict, Union
from typing import Optional

gem_router=APIRouter()  #APIRouter is used to create a router. Dependencies is used to specify the dependencies of the router


@gem_router.get('/gems', tags=['Gems'])  # @ is a decorator, it is used to add functionality to the function
def gems(lte: Optional[int] = None, gte: Optional[int] = None):
    gems_query = select(Gem, GemProperties).join(GemProperties)
    if lte:
        gems_query = gems_query.where(Gem.price <= lte)
    if gte:
        gems_query = gems_query.where(Gem.price >= gte)
        
    gems = session.exec(gems_query).all()
    
    return {'gems': [{'gem': gem, 'props': props} for gem, props in gems]}
    

@gem_router.get('/gem/{id}',response_model=Gem,tags=['Gems'])   # @ is a decorator, it is used to add functionality to the function
def gem(id: int):   
    """GETS GEM BY ID"""
    gem_found=session.get(Gem,id)
    if not gem_found:
        raise HTTPException(status_code=404,detail='Gem not found')
    return gem_found
# def sample_debug():
#     try:
#         gem=gem_repository.select_gem(id)
#         return {'gem':gem}
#     except:
#         logger.debug(traceback.format_exc())
#         return {'error':'Gem not found'}

@gem_router.post('/gems',tags=['Gems']) #post is used to send data to the server
def create_gem(gem_pr: GemProperties,gem: Gem,user=Depends(auth_handler.get_current_user)):        #type declaration is used to specify the type of the parameter. reads body as json and then converts it to the type specified
    """CREATES GEM"""
    if not user.is_seller:
        raise HTTPException(status_code=401,detail='Unauthorized')
    gem_properties=GemProperties(size=gem_pr.size,color=gem_pr.color,
                                 clarity=gem_pr.clarity)

    session.add(gem_properties)
    session.commit()
    gem_=Gem(price=gem.price,available=gem.available,gem_properties=gem_properties,
            gem_properties_id=gem_properties.id,seller_id=user.id,seller=user)
    price=calculate_gem_price(gem,gem_pr)
    gem.price=price
    session.add(gem_)
    session.commit()
    return gem


@gem_router.put('/gems/{id}',response_model=Gem,tags=['Gems'])             #patch is used to update the data

def update_gem(id:int,gem:Gem,user=Depends(auth_handler.get_current_user)):
    """UPDATES GEM"""
    gem_found=session.get(Gem,id)
    if not user.is_seller or gem_found.seller_id!=user.id:
        raise HTTPException(status_code=401,detail='Unauthorized')
        
    update_item_encoded=jsonable_encoder(gem)               #jsonable_encoder is used to convert the    object to json
    update_item_encoded.pop('id',None)                      #pop is used to remove the item with the specified key. None is returned if the key is not found
    for key,val in update_item_encoded.items():
       gem_found.__setattr__(key,val)                       #setattr is used to set the value of the attribute of an object
    session.commit()
    return gem_found


@gem_router.patch('/gems/{id}',response_model=Gem,tags=['Gems'])             #patch is used to update the data. Response model is used to specify the model of the response

def patch_gem(id:int,gem:GemPatch,user=Depends(auth_handler.get_current_user)):
    """PATCHES GEM"""
    gem_found=session.get(Gem,id)
    if not user.is_seller or gem_found.seller_id!=user.id:
        raise HTTPException(status_code=401,detail='Unauthorized')
    update_data=gem.model_dump(exclude_unset=True)               #exclude_unset is used to exclude the fields which are not set
    update_data.pop('id',None)                      #pop is used to remove the item with the specified key. None is returned if the key is not found
    for key,val in update_data.items():
       gem_found.__setattr__(key,val)                       #setattr is used to set the value of the attribute of an object
    session.commit()
    return gem_found


@gem_router.delete('/gems/{id}',status_code=HTTP_204_NO_CONTENT,tags=['Gems'])             #delete is used to delete the data

def delete_gem(id:int,user=Depends(auth_handler.get_current_user)):
    """DELETES GEM"""
    gem_found=session.get(Gem,id)
    if not user.is_seller or gem_found.seller_id!=user.id:
        raise HTTPException(status_code=401,detail='Unauthorized')
    session.delete(gem_found)
    session.commit()


@gem_router.get('/gems/seller/me',tags=['seller'],
                response_model=List[Dict[str,Union[Gem,GemProperties]]])  
def get_seller(user=Depends(auth_handler.get_current_user)):
    """GETS SELLER"""
    if not user.is_seller:
        raise HTTPException(status_code=401,detail='Unauthorized')
    statement=select(Gem,GemProperties).where(Gem.seller_id==user.id).join(GemProperties)
    gems=session.exec(statement).all()
    res=[{'gem':gem,'props':props} for gem,props in gems]
    return res

    # gem_found = session.get(Gem, gem_id)
    # if not gem_found:
    #     raise HTTPException(status_code=404, detail="Gem not found")

    # # Update the gem properties
    # for key, value in gem_data.dict(exclude_unset=True).items():
    #     setattr(gem, key, value)

    # try:
    #     session.commit()
    # except IntegrityError:
    #     session.rollback()
    #     raise HTTPException(status_code=400, detail="Integrity error: Duplicate ID or other constraint violation")
    # return gem
