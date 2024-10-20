#File to populate the database with random data

import random
from db.db import engine    #We import from db since circular import happens if we import from main
from sqlmodel import Session
from models.gem_models import Gem, GemProperties, GemType, GemColor



color_multiplier = {
    'D': 1.8,
    'E': 1.6,
    'G': 1.4,
    'F': 1.2,
    'H': 1,
    'I': 0.8
}

def calculate_gem_price(gem, gem_pr):
    price = 1000
    if gem.gem_type == 'Ruby':
        price = 400
    elif gem.gem_type == 'Emerald':
        price = 650

    if gem_pr.clarity == 1:
        price *= 0.75
    elif gem_pr.clarity == 3:
        price *= 1.25
    elif gem_pr.clarity == 4:
        price *= 1.5

    price = price * (gem_pr.size**3)

    if gem.gem_type == 'Diamond':
        multiplier = color_multiplier[gem_pr.color]
        price *= multiplier

    return price

def create_gem_props():
    size=random.randint(3,70)/10
    color=random.choice(GemColor.list())
    clarity=random.randint(1,5)
    gemp_p=GemProperties(size=size,color=color,clarity=clarity)   #gem_p is an instance of GemProperties
    return gemp_p

def create_gem(gem_p):          #gem_p is an instance of GemProperties
    type=random.choice(GemType.list())
    gem=Gem(price=1000,gem_properties_id=gem_p.id, gem_type=type)   #gem is an instance of Gem
    price=calculate_gem_price(gem,gem_p)
    price=round(price,2)        #
    gem.price=price
    return gem

def create_gems_db():
    # gem_p=create_gem_props()
    gem_ps=[create_gem_props() for i in range(100)]
    print(gem_ps)

    with Session(engine) as session:            #Session is a class in sqlmodel which is used to create a session object, it is used to interact with the database
        session.add_all(gem_ps)
        session.commit()
        gems=[create_gem(gem_ps[i]) for i in range(100)]
        # gem=create_gem(gem_p.id)
        # gem.gem_properties_id
        session.add_all(gems)
        session.commit()            #commit is used to commit the changes to the database
#create_gems_db()
