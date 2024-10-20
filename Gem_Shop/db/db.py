
# from sqlmodel import SQLModel, create_engine

# engine= create_engine('sqlite:///database.db', echo=True)

from sqlmodel import SQLModel, create_engine, Session
eng=r'/Users/eshaan/Desktop/Dev/Trace/Gem_Shop/database.db'
sqlite_url = f"sqlite:///{eng}"
engine= create_engine(sqlite_url, echo=True)
session=Session(bind=engine)
