import azure.functions as func
from typing import Any, Optional
import logging
try:
    from .databases.database import Database
    status = True
except:
    status = False

import json

logger = logging.getLogger(__name__)

def create_error_response(field: str, text: str, value: Any, status_code: int, correct_value: Optional[Any]) -> func.HttpResponse:
    """Constructs an error message based on the field"""
    error_str =f"{field} {text}. Was {value}"
    if correct_value is not None:
        error_str += f" should have been: {correct_value}."
    logging.error(error_str)
    return func.HttpResponse(json.dumps({"status": "failed", "error": error_str}), status_code=status_code)

def parse_input(req: func.HttpRequest, value_name: str) -> Any | None:
    """ Get value from params in http request or from the boy"""
    if (value := req.params.get(value_name)) is not None:
        return value
    try:
        req_body = req.get_json()
        return req_body.get('name')
    except ValueError:
        return None

def parse_login(req: func.HttpRequest, database: Any) -> bool:
    """ Parse request object and tries to login"""
    if (username := parse_input(req, 'username')) is None:
        logging.error(f"Username or password was not given")
        return False
    if (password := parse_input(req, 'password')) is None:
        logging.error(f"Username or password was not given")
        return False
    if (status := database.login(username, password)):
        logging.info("User logged in")
    else:
        logging.error(f"Username or password was incorrect")
    return status