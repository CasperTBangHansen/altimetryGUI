import azure.functions as func
from shared_src import GLOBAL_HEADERS
from shared_src.databases import database
from shared_src.HandleInput import parse_input, create_error_response, parse_login
from os import environ
import json

# Database
DATABASE = database.Database(
    username=environ["ALTIMETRY_USERNAME"],
    password=environ["ALTIMETRY_PASSWORD"],
    host=environ["ALTIMETRY_HOST"],
    port=environ["ALTIMETRY_DATABASE_PORT"],
    database_name=environ["ALTIMETRY_DATABASE"],
    engine=environ["ALTIMETRY_DATABASE_CONNECTION_ENGINE"],
    database_type=environ["ALTIMETRY_DATABASE_TYPE"],
    create_tables=environ["ALTIMETRY_CREATE_TABLES"] == 'true'
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    # login
    if not parse_login(req, DATABASE):
        return func.HttpResponse(
            json.dumps({"status": "failed", "error": "Username or password was not passed or where incorrect"}),
            status_code=400,
            headers=GLOBAL_HEADERS
        )
    # Get parameters and check them
    if (resolution_name := parse_input(req, 'name')) is None:
        return create_error_response("name", "has an invalid format", resolution_name, 400, "'string'")
    if len(resolution_name) > 30:
         return create_error_response("name", "is too long.", resolution_name, 400, "less than 30 characters")
    if len(resolution_name) == 0:
        return create_error_response("name", "is empty.", resolution_name, 400, "between 1-30 characters")

    if (resolution := DATABASE.get_resolutions_by_name(resolution_name)) is None:
        return create_error_response('name', "did not exist in the database", resolution, 400, "Other name")

    # remove resolution from database
    if DATABASE.delete_resolutions(resolution_id=resolution.id):
        return func.HttpResponse(json.dumps({"status": "success"}), status_code = 200, headers=GLOBAL_HEADERS)
    return func.HttpResponse(
        json.dumps({"status": "failed", "error": "Failed to remove resolution from database"}),
        status_code = 404,
        headers=GLOBAL_HEADERS
    )
