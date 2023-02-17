import azure.functions as func
from shared_src.databases import database, tables
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
            status_code=404
        )

    # Get parameters and check them
    if (product_name := parse_input(req, 'name')) is None:
        return create_error_response("name", "has an invalid format", product_name, 400, "'string'")
    if len(product_name) > 30:
         return create_error_response("name", "is too long.", product_name, 400, "less than 30 characters")
    if len(product_name) == 0:
        return create_error_response("name", "is empty.", product_name, 400, "between 1-30 characters")

    # Add product to database
    if (DATABASE.add_product(tables.Product(name=product_name))):
        return func.HttpResponse(json.dumps({"status": "success"}), status_code = 200)
    return func.HttpResponse(
        json.dumps({"status": "failed", "error": f"Failed to add product to database ({product_name} probably already exists in the database)"}),
        status_code = 404
    )
    
