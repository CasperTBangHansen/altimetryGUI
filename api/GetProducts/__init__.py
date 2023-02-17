import azure.functions as func
from shared_src.databases import database
from shared_src.HandleInput import parse_input
from os import environ
from typing import Any
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

def check_resolution(resolution: Any | None) -> bool:
    """ Check if resolution was defined and if it is true"""
    if resolution is None:
        return False
    
    if isinstance(resolution, bool):
        return resolution
    
    if isinstance(resolution, str):
        return (
            resolution.lower() in ['true', '1', 't', 'y', 'yes']
        )
    return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    resolution = parse_input(req, "resolution")
    
    # Get resolution if requested
    try:
        if check_resolution(resolution):
            products = DATABASE.get_product_and_resolutions()
            response_type = "both"
        else:
            # Get products from the database
            products = DATABASE.get_product_names()
            response_type = "product"
        return func.HttpResponse(json.dumps({"status": "success", "type": response_type, "products": products}), status_code = 200)
    except:
        return func.HttpResponse(json.dumps({"status": "failed"}), status_code = 500)
    
