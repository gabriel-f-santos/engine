import json
import db_session
from http import HTTPStatus
from models import Tenant
import bcrypt
import secrets


def lambda_handler(event, context):
    body = json.loads(event["body"])
    password = bcrypt.hashpw(body["password"].encode("utf-8"), bcrypt.gensalt())

    api_key = secrets.token_hex(16)
    tenant = Tenant(
        name=body["name"],
        email=body["email"],
        password=password,
        api_key=api_key,
    )

    with db_session.create_session() as session:
        if session.query(Tenant).filter_by(email=body["email"]).first():
            return {
                "statusCode": HTTPStatus.CONFLICT.value,
                "body": json.dumps({"message": "Error creating tenant"}),
            }

        session.add(tenant)
        session.commit()

    return {
        "statusCode": HTTPStatus.CREATED.value,
        "body": json.dumps({"message": "Tenant created sucessfully"}),
    }
