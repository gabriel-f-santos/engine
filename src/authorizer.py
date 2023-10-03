import jwt
import settings
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"Received event {event}")

    authorization = event["headers"].get("Authorization")

    authResponse = {
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": event["methodArn"],
                }
            ],
        },
    }

    if authorization:
        return check_jwt_auth(authorization, authResponse)

    authResponse["policyDocument"]["Statement"][0]["Effect"] = "Deny"
    return authResponse


def check_jwt_auth(token, authResponse):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        authResponse["context"] = {"tenant_id": payload["tenant_id"]}
        authResponse["principalId"] = payload["sub"]
        return authResponse
    except Exception:
        authResponse["principalId"] = ("unauthenticated",)
        authResponse["policyDocument"]["Statement"][0]["Effect"] = "Deny"
        return authResponse
