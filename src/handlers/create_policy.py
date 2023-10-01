import json
from http import HTTPStatus
from src.models import db_session, Partner, Policy


def lambda_handler(event, context):
    body = json.loads(event["body"])
    with db_session.create_session() as session:
        partner = (
            session.query(Partner)
            .filter_by(partner_id=body["partner_id"])
            .first()
        )

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

    policy = Policy(
        name=body["name"],
        partner_id=body["partner_id"],
        policy_details=body["policy_details"],
    )
    with db_session.create_session() as session:
        session.add(policy)
        session.commit()

    return {
        "statusCode": HTTPStatus.CREATED.value,
        "body": json.dumps({"message": "policy created"}),
    }
