import os
from alembic.config import Config
from alembic import command

from models import Base
from db_session import create_engine


def lambda_handler(event, context):
    engine = create_engine()
    Base.metadata.create_all(engine)

    return {"statusCode": 200, "body": "Migrations applied successfully!"}
