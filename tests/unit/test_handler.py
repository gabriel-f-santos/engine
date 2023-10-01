import json
import unittest
from http import HTTPStatus
from src.handlers import create_policy
from src.models import db_session, Partner, Policy


class TestLambdaHandler(unittest.TestCase):
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
                    "partner_id": cls.partner_id,
                    "policy_details": {
                        "1": {"rule": "gt", "field": "age", "threshold": 20}
                    },
                }
            ),
            "resource": "/{proxy+}",
        }

    @classmethod
    def tearDownClass(cls):
        with db_session.create_session() as session:
            session.query(Partner).delete()
            session.commit()

    def test_successful_policy_creation(self):
        context = {}
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
                "partner_id": 999,
                "policy_details": {
                    "1": {"rule": "gt", "field": "age", "threshold": 20}
                },
            }
        )

        context = {}
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

        context = {}
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
