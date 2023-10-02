import json
from http import HTTPStatus
from datetime import datetime, timedelta
from src.models import Tenant
from src import settings, db_session
import jwt
import bcrypt


def lambda_handler(event, context):
    body = json.loads(event["body"])

    with db_session.create_session() as session:
        tenant = session.query(Tenant).filter_by(email=body["email"]).first()

    match_password = bcrypt.checkpw(
        body["password"].encode("utf-8"), tenant.password
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
