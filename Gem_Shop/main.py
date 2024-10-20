import traceback
from fastapi import FastAPI, HTTPException
import uvicorn   #Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools.
from populate import calculate_gem_price
from repos import gem_repository
from sqlmodel import SQLModel,create_engine,Session
from db.db import engine
from models.gem_models import *     #importing all the classes from gem_models.py
# from loguru import logger
from endpoints.gem_endpoints import gem_router
from endpoints.user_endpoints import user_router
app=FastAPI()
app.include_router(gem_router)              #include_router is used to include the router in the app. We register the router with the app
app.include_router(user_router)  
eng= r'/Users/eshaan/Desktop/Dev/Trace/Gem_Shop/database.db'     #Giving full path because 
sqlite_url=f'sqlite:///{eng}'
engine=create_engine(sqlite_url,echo=True)             #Echo is used to print the SQL queries being executed


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)





if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000,reload=True,) #reload=True is used to reload the server when the code is changed
    # create_db_and_tables()


