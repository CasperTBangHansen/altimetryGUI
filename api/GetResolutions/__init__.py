import azure.functions as func
from shared_src import GLOBAL_HEADERS
from shared_src.databases import database, tables
from shared_src.HandleInput import parse_input, create_error_response
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
    # Get product name or id
    product_name = parse_input(req, 'name')
    product_id = parse_input(req, 'id')
    if product_name is None and product_id is None:
        return create_error_response(
            "name and id",
            "has an invalid format",
            f"{product_name} and {product_id}",
            400,
            "a string for the name or an int for the id. Only one of these values has to be specified"
        )

    # Get resolutions from the database
    try:
        resolutions = DATABASE.get_resolutions_by_product(product_name=product_name, product_id=product_id)
        if resolutions is None:
            return func.HttpResponse(json.dumps({"status": "failed", "error": "product did not exist"}), status_code = 400, headers=GLOBAL_HEADERS)
        
        # If successfull format the resolution table
        resolution_dict = tables.get_fields_as_dict(resolutions)
        return func.HttpResponse(json.dumps({"status": "success", "resolutions": resolution_dict}), status_code = 200, headers=GLOBAL_HEADERS)
    except ValueError as e:
        return func.HttpResponse(json.dumps({"status": "failed", "error": e}), status_code = 400, headers=GLOBAL_HEADERS)