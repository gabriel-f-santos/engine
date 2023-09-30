import json
from src.models.db_session import create_session
from src.models import User
# import requests

session = create_session()

def lambda_handler(event, context):
    query = session.query(User)
    print(query.count())
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "hello world"}),
    }
