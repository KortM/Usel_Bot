import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

name = 'BD.db'
engine = create_engine("sqlite:///"+name, connect_args={'check_same_thread': False})
Base = declarative_base()
Session =sessionmaker(bind= engine)

class Usel(Base):
    __tablename__ = 'Usel'
    id = Column(Integer, primary_key=True)
    description = Column(String(500))

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "{0}".format(self.description)

#Base.metadata.create_all(engine)