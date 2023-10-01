import json
from http import HTTPStatus
from src.models import db_session, Partner
import bcrypt


def lambda_handler(event, context):
    body = json.loads(event["body"])
    password = bcrypt.hashpw(body["password"].encode(), bcrypt.gensalt())

    partner = Partner(name=body["name"], email=body["email"], password=password)

    with db_session.create_session() as session:
        partner = session.query(Partner).filter_by(email=body["email"]).first()
        if partner:
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
