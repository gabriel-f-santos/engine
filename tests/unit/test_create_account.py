from http import HTTPStatus
import json
import unittest
from src.handlers import create_partner
from src.models import db_session, Partner


class TestCreatePartnerHandler(unittest.TestCase):
    def setUp(self):
        self.email = "partner@example.com"
        self.event = {
            "body": json.dumps(
                {
                    "name": "partner name",
                    "email": self.email,
                    "password": "123password",
                }
            ),
            "resource": "/{proxy+}",
            "requestContext": {
                "resourceId": "123456",
                "apiId": "1234567890",
                "resourcePath": "/{proxy+}",
                "httpMethod": "POST",
                "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
                "accountId": "123456789012",
                "identity": {
                    "apiKey": "",
                    "userArn": "",
                    "cognitoAuthenticationType": "",
                    "caller": "",
                    "userAgent": "Custom User Agent String",
                    "user": "",
                    "cognitoIdentityPoolId": "",
                    "cognitoIdentityId": "",
                    "cognitoAuthenticationProvider": "",
                    "sourceIp": "127.0.0.1",
                    "accountId": "",
                },
                "stage": "prod",
            },
            "queryStringParameters": {"foo": "bar"},
            "headers": {
                "Via": "1.1 08f323deadbeefa7af34d5feb414nt)",
                "Accept-Language": "en-US,en;q=0.8",
                "CloudFront-Is-Desktop-Viewer": "true",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "CloudFront-Is-Mobile-Viewer": "false",
                "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
                "CloudFront-Viewer-Country": "US",
                "Accept": "text/html,application/xhtml+xml",
                "Upgrade-Insecure-Requests": "1",
                "X-Forwarded-Port": "443",
                "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
                "X-Forwarded-Proto": "https",
                "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jNLmGJHqlaA==",
                "CloudFront-Is-Tablet-Viewer": "false",
                "Cache-Control": "max-age=0",
                "User-Agent": "Custom User Agent String",
                "CloudFront-Forwarded-Proto": "https",
                "Accept-Encoding": "gzip, deflate, sdch",
            },
            "pathParameters": {"proxy": "/examplepath"},
            "httpMethod": "POST",
            "stageVariables": {"baz": "qux"},
            "path": "/examplepath",
        }

    def tearDown(self):
        with db_session.create_session() as session:
            session.query(Partner).delete()
            session.commit()

    def test_successful_create(self):
        context = {}
        response = create_partner.lambda_handler(self.event, context)

        with db_session.create_session() as session:
            partner = session.query(Partner).filter_by(email=self.email).first()

        self.assertEqual(response["statusCode"], HTTPStatus.CREATED.value)
        self.assertEqual(partner.email, self.email)

    def test_failed_login(self):
        partner = Partner(
            name="name",
            email="partner@example.com",
            password="wrong_password",
        )

        with db_session.create_session() as session:
            session.add(partner)
            session.commit()

        context = {}
        response = create_partner.lambda_handler(self.event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.CONFLICT.value)
