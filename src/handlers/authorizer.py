import jwt
from src import settings


def lambda_handler(event, context):
    token = event["headers"]["Authorization"]

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

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        authResponse["context"] = {"tenant_id": payload["tenant_id"]}
        authResponse["principalId"] = (payload["sub"],)
        return authResponse
    except Exception:
        authResponse["principalId"] = ("unauthenticated",)
        authResponse["policyDocument"]["Statement"][0]["Effect"] = ("Deny",)
        return authResponse
