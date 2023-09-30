from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # Table name in the database
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)