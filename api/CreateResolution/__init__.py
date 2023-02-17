import azure.functions as func
from shared_src.databases import database, tables
from shared_src.HandleInput import parse_input, create_error_response, parse_login
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


def parse_name(req: func.HttpRequest, param: str) -> func.HttpResponse | Any:
    """Check and converts request object with param name to the correct type or response."""
    # Get parameters and check them
    if (out_name := parse_input(req, param)) is None:
        return create_error_response(param, "has an invalid format", out_name, 400, "'string'")
    if len(out_name) > 30:
         return create_error_response(param, "is too long.", out_name, 400, "less than 30 characters")
    if len(out_name) == 0:
        return create_error_response(param, "is empty.", out_name, 400, "between 1-30 characters")
    return out_name

def main(req: func.HttpRequest) -> func.HttpResponse:
    # login
    if not parse_login(req, DATABASE):
        return func.HttpResponse(
            json.dumps({"status": "failed", "error": "Username or password was not passed or where incorrect"}),
            status_code=404
        )

    # Resolution name
    if isinstance((resolution := parse_name(req, 'name')), func.HttpResponse):
        return resolution
    # Product name
    if isinstance((product := parse_name(req, 'product_name')), func.HttpResponse):
        return product
    # x
    if (x := parse_input(req, 'x')) is None or isinstance(x, (float, int)):
         return create_error_response('x', "has an invalid format", x, 400, "'int' or 'float'")
    # y
    if (y := parse_input(req, 'y')) is None or isinstance(y, (float, int)): 
         return create_error_response('y', "has an invalid format", y, 400, "'int' or 'float'")
    # time_days
    if (time := parse_input(req, 'time')) is None or isinstance(time, int): 
        return create_error_response('time', "has an invalid format", time, 400, "'int'")

    # Get product with product name
    if (prod := DATABASE.get_product_by_name(product)) is None:
        product_names = DATABASE.get_product_names()
        return create_error_response('product_name', "did not exist in the database", prod, 400, " ".join(product_names))

    # Add resolution to database
    resolution = tables.Resolution(
        name=resolution,
        x=x,
        y=y,
        time_days=time,
        product_id=prod.id
    )
    status, response = DATABASE.add_resolution(resolution)
    if (status):
        return func.HttpResponse(json.dumps({"status": "success"}), status_code = 200)
    return func.HttpResponse(
        json.dumps({"status": "failed", "error": response}),
        status_code = 404
    )
