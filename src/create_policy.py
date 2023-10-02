import json
from http import HTTPStatus
from models import Tenant, Policy
import db_session


def lambda_handler(event, context):
    body = json.loads(event["body"])
    tenant_id = context["authorizer"].get("tenant_id")
    with db_session.create_session() as session:
        tenant = session.query(Tenant).filter_by(id=tenant_id).first()

    if tenant is None:
        return {
            "statusCode": HTTPStatus.FORBIDDEN.value,
            "body": json.dumps({"message": "forbidden"}),
        }

    if not tenant.is_active:
        return {
            "statusCode": HTTPStatus.UNAUTHORIZED.value,
            "body": json.dumps({"message": "forbidden"}),
        }
    with db_session.create_session() as session:
        existing_policy = (
            session.query(Policy).filter_by(tenant_id=tenant_id).first()
        )

        if existing_policy:
            existing_policy.name = body["name"]
            existing_policy.policy_details = body["policy_details"]
            session.merge(existing_policy)
        else:
            policy = Policy(
                name=body["name"],
                tenant_id=tenant_id,
                policy_details=body["policy_details"],
            )

            session.add(policy)
            session.commit()

    return {
        "statusCode": HTTPStatus.CREATED.value,
        "body": json.dumps({"message": "policy created"}),
    }
