import logging
import json
from typing import Dict
from src.evm.addresses import CONNECTORS

logger = logging.getLogger(__name__)

def supervisor_rule(strategy: Dict) -> str:
    """
    Validate the generated strategy using supervisor rules and return a structured JSON string with status and feedback.

    Args:
        strategy (Dict): The strategy to validate.

    Returns:
        str: A structured JSON string containing 'status' (valid/invalid/error) and detailed 'feedback'.
    """
    validation_response = {
        "status": "valid",
        "feedback": {
            "errorType": None,
            "message": "Strategy is valid and meets the requirements."
        }
    }
 
    if not strategy:
        validation_response["status"] = "error"
        validation_response["feedback"] = {
            "errorType": "MissingStrategy",
            "message": "No strategy found. Please generate a new single-step strategy following the defined JSON format."
        }
        return json.dumps(validation_response)

    if "steps" not in strategy:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "MissingSteps",
            "message": (
                "Generated strategy is missing the 'steps' key. Ensure the strategy includes a valid 'steps' field "
                "with exactly one step in the required format."
            )
        }
        return json.dumps(validation_response)

    if len(strategy["steps"]) != 1:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "InvalidStepsCount",
            "message": (
                f"Strategy contains {len(strategy['steps'])} steps instead of one. Regenerate the strategy "
                "to include exactly one step as required."
            )
        }
        return json.dumps(validation_response)

    required_keys = ["name", "description", "minDeposit"]
    missing_keys = [key for key in required_keys if key not in strategy]
    if missing_keys:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "MissingKeys",
            "message": (
                f"Generated strategy is missing required keys: {', '.join(missing_keys)}. Ensure these fields are included and properly formatted."
            )
        }
        return json.dumps(validation_response)

    step = strategy["steps"][0]
    required_step_keys = ["connector", "actionType", "assetsIn", "assetOut", "amountRatio", "data"]
    missing_step_keys = [key for key in required_step_keys if key not in step]
    if missing_step_keys:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "MissingStepKeys",
            "message": (
                f"Generated strategy step is missing required keys: {', '.join(missing_step_keys)}. "
                "Ensure these fields are included and properly formatted in the step."
            )
        }
        return json.dumps(validation_response)

    connector = step["connector"]
    protocol = strategy.get("protocol", "").lower()
    if protocol not in CONNECTORS:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "InvalidProtocol",
            "message": f"Invalid protocol: {protocol}. Supported protocols are: {', '.join(CONNECTORS.keys())}."
        }
        return json.dumps(validation_response)

    expected_connector = CONNECTORS[protocol]
    if connector != expected_connector:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "InvalidConnector",
            "message": f"Invalid connector for protocol {protocol}: {connector}. Expected: {expected_connector}."
        }
        return json.dumps(validation_response)

    assets_in = step.get("assetsIn", [])
    asset_out = step.get("assetOut")
    if not assets_in or not asset_out:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "InvalidAssets",
            "message": "AssetsIn or AssetOut are missing or empty. Ensure both are properly set."
        }
        return json.dumps(validation_response)

    amount_ratio = step.get("amountRatio")
    if not str(amount_ratio).isdigit() or int(amount_ratio) < 1 or int(amount_ratio) > 10000:
        validation_response["status"] = "invalid"
        validation_response["feedback"] = {
            "errorType": "InvalidAmountRatio",
            "message": (
                f"Invalid amount ratio: {amount_ratio}. Ensure the value is an integer between 1 and 10000."
            )
        }
        return json.dumps(validation_response)

    validation_response["status"] = "valid"
    validation_response["feedback"]["message"] = "Strategy is valid and meets the requirements."
    return json.dumps(validation_response)
