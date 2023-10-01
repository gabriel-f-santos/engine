import jwt


def lambda_handler(event, context):
    token = event["headers"]["Authorization"]
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return {
            "principalId": payload["sub"],
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
    except Exception:
        return {
            "principalId": "unauthenticated",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Deny",
                        "Resource": event["methodArn"],
                    }
                ],
            },
        }
