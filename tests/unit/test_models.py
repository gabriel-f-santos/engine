import unittest
from src.models import Tenant, Policy
from src import db_session


class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        with db_session.create_session() as session:
            session.query(Tenant).delete()
            session.commit()

    def test_tenant_model(self):
        tenant = Tenant(name="Tenant Name", email="tenant@example.com")
        with db_session.create_session() as session:
            session.add(tenant)
            session.commit()
            retrieved_tenant = (
                session.query(Tenant).filter_by(id=tenant.id).first()
            )

        self.assertEqual(retrieved_tenant.name, "Tenant Name")

    def test_policy_model(self):
        policy = Policy(
            name="Policy Name",
            tenant_id=1,
            policy_details={
                "1": {"condition": "gt", "field": "age", "threshold": 20}
            },
        )
        with db_session.create_session() as session:
            session.add(policy)
            session.commit()
            retrieved_policy = (
                session.query(Policy).filter_by(id=policy.id).first()
            )

        self.assertEqual(retrieved_policy.name, "Policy Name")
