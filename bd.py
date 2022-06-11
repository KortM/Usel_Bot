import os
from unicodedata import name
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib, uuid

usel_db = 'BD.db'
#basedir =os.path.abspath(os.path.dirname(__file__))
engine = create_engine("sqlite:///{}".format(usel_db), connect_args={'check_same_thread': False})
users_db = 'Users.db'
user_engine = create_engine("sqlite:///{}".format(users_db), connect_args={'check_same_thread': False})
Base = declarative_base()
Session =sessionmaker(bind= engine)
User_session = sessionmaker(bind=user_engine)

class Usel(Base):

    __tablename__ = 'Usel'

    id = Column(Integer, primary_key=True)
    description = Column(String(500))

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "{0}".format(self.description)

    def lenght(self):
        return len(self.description)

class User(Base):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    pwd_hash = Column(String(550))

    def __init_(self, name: str):
        self.name = name
    
    def __repr__(self) -> str:
        return 'User: {}, PWD: {}'.format(self.name, self.pwd_hash)
    
    def set_password(self, password):
        self.pwd_hash = hashlib.sha256(''.join([password]).encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        key = hashlib.sha256(''.join([password]).encode('utf-8')).hexdigest()
        if key == self.pwd_hash:
            return True
        else:
            return False

class AccessUsers(Base):
    
    __tablename__ = 'AccessUsers'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String(200))

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
    
    def __repr__(self) -> str:
        return self.chat_id



Base.metadata.create_all(user_engine)

#Создаем адмнистративного пользователя, через которого будет выполнен вход. 
admin = User(name='support')
admin.set_password('J4cG9CgjCjpH')
admin.check_password('J4cG9CgjCjpH')
user_session = User_session()
user_session.add(admin)
user_session.commit()

