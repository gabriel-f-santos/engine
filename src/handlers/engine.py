import json
from http import HTTPStatus
from src.models import db_session, Policy
import operator

comparison_operators = {
    "gt": operator.gt,
    "gte": operator.ge,
    "lt": operator.lt,
    "lte": operator.le,
    "eq": operator.eq,
    "ne": operator.ne,
}


def evaluate_field(value_to_evaluate, condition, threshold):
    comparison_function = comparison_operators[condition]
    return comparison_function(value_to_evaluate, threshold)


def lambda_handler(event, context):
    partner_id = context["authorizer"]["partner_id"]
    body = json.loads(event["body"])

    with db_session.create_session() as session:
        policy = session.query(Policy).filter_by(id=partner_id).first()
        policy_details = policy.policy_details

    for index, policy in policy_details.items():
        field = policy["field"]
        condition = policy["condition"]
        threshold = policy["threshold"]

        value_to_evaluate = body[field]
        result = evaluate_field(value_to_evaluate, condition, threshold)

        if not result:
            break

    return {
        "statusCode": HTTPStatus.OK.value,
        "body": json.dumps({"decision": result}),
    }
