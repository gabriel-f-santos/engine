from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    api_key = Column(String)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)


class Policy(Base):
    __tablename__ = "policy"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    partner_id = Column(Integer, ForeignKey("partners.id"))
    policy_details = Column(JSON)  # JSON field for policy details
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)

    # Define the relationship with the Partner model
    partner = relationship("Partner")
