from models import Tenant
import db_session


def lambda_handler(event, context):
    api_key = event["headers"].get("x-api-key")

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

    if api_key:
        return check_api_key_auth(api_key, authResponse)

    authResponse["policyDocument"]["Statement"][0]["Effect"] = "Deny"
    return authResponse


def check_api_key_auth(api_key, authResponse):
    with db_session.create_session() as session:
        tenant = session.query(Tenant).filter_by(api_key=api_key).first()

        if tenant is None:
            authResponse["principalId"] = "unauthenticated"
            authResponse["policyDocument"]["Statement"][0]["Effect"] = "Deny"
            return authResponse

        authResponse["context"] = {"tenant_id": tenant.id}
        return authResponse
