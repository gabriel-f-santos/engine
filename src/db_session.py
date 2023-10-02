import os
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker

from pathlib import Path  # Usado no SQLite
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine
import settings

__engine: Optional[Engine] = None


def create_engine():
    """
    Função para configurar a conexão ao banco de dados.
    """
    global __engine

    if __engine:
        return __engine
    
    if settings.DEBUG:

        # import ipdb;ipdb.set_trace()
        db_path = f"sqlite:///src/mydatabase.db"
        __engine = sa.create_engine(url=db_path, echo=False, connect_args={"check_same_thread": False})
    else:
        conn_str = settings.DB_CONNECT
        __engine = sa.create_engine(url=conn_str, echo=False)
    
    return __engine

def create_session() -> Session:
    """
    Função para criar sessão de conexao ao banco de dados.
    """
    global __engine

    if not __engine:
        create_engine()

    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session
