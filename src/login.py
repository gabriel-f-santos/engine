import json
from http import HTTPStatus
from datetime import datetime, timedelta
from models import Tenant
import settings, db_session
import jwt
import bcrypt
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    body = json.loads(event["body"])

    logger.info(f"Received body {body}")

    with db_session.create_session() as session:
        tenant = session.query(Tenant).filter_by(email=body["email"]).first()

    match_password = bcrypt.checkpw(
        body["password"].encode(), tenant.password.encode()
    )

    if match_password:
        token = jwt.encode(
            {
                "tenant_id": tenant.id,
                "apiKey": tenant.api_key,
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
