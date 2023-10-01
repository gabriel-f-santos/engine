import unittest
from src.models import db_session, Partner, Policy


class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        with db_session.create_session() as session:
            session.query(Partner).delete()
            session.commit()

    def test_partner_model(self):
        partner = Partner(name="Partner Name", email="partner@example.com")
        with db_session.create_session() as session:
            session.add(partner)
            session.commit()
            retrieved_partner = (
                session.query(Partner).filter_by(id=partner.id).first()
            )

        self.assertEqual(retrieved_partner.name, "Partner Name")

    def test_policy_model(self):
        policy = Policy(
            name="Policy Name",
            partner_id=1,
            policy_details={
                "1": {"rule": "gt", "field": "age", "threshold": 20}
            },
        )
        with db_session.create_session() as session:
            session.add(policy)
            session.commit()
            retrieved_policy = (
                session.query(Policy).filter_by(id=policy.id).first()
            )

        self.assertEqual(retrieved_policy.name, "Policy Name")
