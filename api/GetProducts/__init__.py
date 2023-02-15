import azure.functions as func
from ..shared_src.databases import database
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
    # Get products from the database
    products = DATABASE.get_product_names()
    return func.HttpResponse(json.dumps({"status": "success", "products": products}), status_code = 200)

    
