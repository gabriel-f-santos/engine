import json
from http import HTTPStatus
from src.models import db_session, Partner, Policy


def lambda_handler(event, context):
    body = json.loads(event["body"])
    partner_id = context["authorizer"].get("partner_id")
    with db_session.create_session() as session:
        partner = session.query(Partner).filter_by(id=partner_id).first()

    if partner is None:
        return {
            "statusCode": HTTPStatus.FORBIDDEN.value,
            "body": json.dumps({"message": "forbidden"}),
        }

    if not partner.is_active:
        return {
            "statusCode": HTTPStatus.UNAUTHORIZED.value,
            "body": json.dumps({"message": "forbidden"}),
        }
    with db_session.create_session() as session:
        existing_policy = (
            session.query(Policy).filter_by(partner_id=partner_id).first()
        )

        if existing_policy:
            existing_policy.name = body["name"]
            existing_policy.policy_details = body["policy_details"]
            session.merge(existing_policy)
        else:
            policy = Policy(
                name=body["name"],
                partner_id=partner_id,
                policy_details=body["policy_details"],
            )

            session.add(policy)
            session.commit()

    return {
        "statusCode": HTTPStatus.CREATED.value,
        "body": json.dumps({"message": "policy created"}),
    }
