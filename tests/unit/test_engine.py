import json
import unittest
from http import HTTPStatus
from src import engine, db_session
from src.models import Tenant, Policy


class TestCreateHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tenant = Tenant(name="Tenant Name", email="tenant@example.com")

        with db_session.create_session() as session:
            session.add(tenant)
            session.commit()

        cls.tenant_id = tenant.id

        policy = Policy(
            name="Policy Name",
            tenant_id=cls.tenant_id,
            policy_details={
                "1": {"condition": "gt", "field": "age", "threshold": 20},
                "2": {"condition": "gte", "field": "income", "threshold": 1000},
            },
        )
        with db_session.create_session() as session:
            session.add(policy)
            session.commit()

        cls.event = {
            "body": json.dumps({"age": 23, "income": 3000}),
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
            session.query(Tenant).delete()
            session.query(Policy).delete()
            session.commit()

    def test_successful_engine_evaluation(self):
        context = {"authorizer": {"tenant_id": self.tenant_id}}

        response = engine.lambda_handler(self.event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.OK.value)
        expected_body = json.dumps({"decision": True})
        self.assertEqual(response["body"], expected_body)

    def test_rejected_age_engine_evaluation(self):
        context = {"authorizer": {"tenant_id": self.tenant_id}}

        self.event["body"] = json.dumps({"age": 20, "income": 3000})
        response = engine.lambda_handler(self.event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.OK.value)
        expected_body = json.dumps({"decision": False})
        self.assertEqual(response["body"], expected_body)

    def test_rejected_income_engine_evaluation(self):
        context = {"authorizer": {"tenant_id": self.tenant_id}}

        self.event["body"] = json.dumps({"age": 21, "income": 1000})
        response = engine.lambda_handler(self.event, context)

        self.assertEqual(response["statusCode"], HTTPStatus.OK.value)
        expected_body = json.dumps({"decision": True})
        self.assertEqual(response["body"], expected_body)
