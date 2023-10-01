import json
from http import HTTPStatus
from datetime import datetime, timedelta
from src.models import db_session, Partner
from src import settings
import jwt
import bcrypt


def lambda_handler(event, context):
    body = json.loads(event["body"])

    with db_session.create_session() as session:
        partner = session.query(Partner).filter_by(email=body["email"]).first()

    match_password = bcrypt.checkpw(
        body["password"].encode("utf-8"), partner.password
    )

    if match_password:
        token = jwt.encode(
            {
                "partner_id": partner.id,
                "exp": datetime.utcnow() + timedelta(days=5),
            },
            settings.JWT_SECRET,
            algorithm="HS256",
        )

        return {
            "statusCode": HTTPStatus.OK.value,
            "body": json.dumps({"token": token}),
        }

    return {
        "statusCode": HTTPStatus.UNAUTHORIZED.value,
        "body": json.dumps({"message": "Invalid password or email"}),
    }
