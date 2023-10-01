import json
from http import HTTPStatus
from src.models import db_session, Partner
import bcrypt
import secrets


def lambda_handler(event, context):
    body = json.loads(event["body"])
    password = bcrypt.hashpw(body["password"].encode(), bcrypt.gensalt())

    api_key = secrets.token_hex(16)
    partner = Partner(
        name=body["name"],
        email=body["email"],
        password=password,
        api_key=api_key,
    )

    with db_session.create_session() as session:
        if session.query(Partner).filter_by(email=body["email"]).first():
            return {
                "statusCode": HTTPStatus.CONFLICT.value,
                "body": json.dumps({"message": "Error creating partner"}),
            }

        session.add(partner)
        session.commit()

    return {
        "statusCode": HTTPStatus.CREATED.value,
        "body": json.dumps({"message": "Partner created sucessfully"}),
    }
