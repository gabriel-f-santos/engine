import jwt


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
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        authResponse["context"] = {"partner_id": payload["partner_id"]}
        authResponse["principalId"] = (payload["sub"],)
        return authResponse
    except Exception:
        authResponse["principalId"] = ("unauthenticated",)
        authResponse["policyDocument"]["Statement"][0]["Effect"] = ("Deny",)
        return authResponse
