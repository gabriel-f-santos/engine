import json
import unittest
from http import HTTPStatus
from src.handlers import create_policy
from src.models import db_session, Partner, Policy


class TestCreateHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        partner = Partner(name="Partner Name", email="partner@example.com")
        with db_session.create_session() as session:
            session.add(partner)
            session.commit()
        cls.partner_id = partner.id

        cls.event = {
            "body": json.dumps(
                {
                    "name": "Policy Name",
                    "policy_details": {
                        "1": {
                            "condition": "gt",
                            "field": "age",
                            "threshold": 20,
                        }
                    },
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

    @classmethod
    def tearDownClass(cls):
        with db_session.create_session() as session:
            session.query(Partner).delete()
            session.commit()

    def test_successful_policy_creation(self):
        context = {"authorizer": {"partner_id": self.partner_id}}
        response = create_policy.lambda_handler(self.event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.CREATED.value)
        expected_body = json.dumps({"message": "policy created"})
        self.assertEqual(response["body"], expected_body)

        with db_session.create_session() as session:
            created_policy = (
                session.query(Policy).filter_by(name="Policy Name").first()
            )
            self.assertIsNotNone(created_policy)
            self.assertEqual(created_policy.partner_id, self.partner_id)

    def test_forbidden_request(self):
        event = self.event.copy()
        event["body"] = json.dumps(
            {
                "name": "Policy Name",
                "policy_details": {
                    "1": {"condition": "gt", "field": "age", "threshold": 20}
                },
            }
        )

        context = {"authorizer": {"partner_id": 999}}
        response = create_policy.lambda_handler(event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.FORBIDDEN.value)
        expected_body = json.dumps({"message": "forbidden"})
        self.assertEqual(response["body"], expected_body)

    def test_unauthorized_request(self):
        with db_session.create_session() as session:
            partner = (
                session.query(Partner).filter_by(id=self.partner_id).first()
            )
            partner.is_active = False
            session.commit()

        context = {"authorizer": {"partner_id": self.partner_id}}
        response = create_policy.lambda_handler(self.event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.UNAUTHORIZED.value)
        expected_body = json.dumps({"message": "forbidden"})
        self.assertEqual(response["body"], expected_body)

        with db_session.create_session() as session:
            partner = (
                session.query(Partner).filter_by(id=self.partner_id).first()
            )
            partner.is_active = True
            session.commit()
