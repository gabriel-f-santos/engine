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


class Tenant(Base):
    __tablename__ = "tenants"

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
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    policy_details = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    tenant = relationship("Tenant")
