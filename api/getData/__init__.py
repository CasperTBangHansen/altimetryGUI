import azure.functions as func
from shared_src import GLOBAL_HEADERS, xarray_operations
import logging
from typing import Optional, Any
from datetime import datetime, date
from shared_src.HandleInput import create_error_response, parse_input
from shared_src.databases import database, tables
import zipfile
import io

from os import environ
import json

# Logging
logging.getLogger(__name__)

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
    if len(out_name) > 50:
         return create_error_response(param, "is too long.", out_name, 400, "less than 50 characters")
    if len(out_name) == 0:
        return create_error_response(param, "is empty.", out_name, 400, "between 1-50 characters")
    return out_name

def parse_date(req: func.HttpRequest, param: str) -> func.HttpResponse | Any:
    """Check and converts request object with param name to the correct type or response."""
    # Get parameters and check them
    if (date_str := parse_input(req, param)) is None:
        return create_error_response(param, "has an invalid format", date_str, 400, "'YYYY-mm-dd'")
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return create_error_response(param, "has an invalid format", date_str, 400, "'YYYY-mm-dd'")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Requesting data")
    # Resolution name
    if isinstance((resolution := parse_name(req, 'resolution_name')), func.HttpResponse):
        return resolution
    
    # Product name
    if isinstance((product := parse_name(req, 'product_name')), func.HttpResponse):
        return product
    
    # Start date
    if isinstance((start_date := parse_date(req, 'start_date')), func.HttpResponse):
        return start_date
    
    # End date
    if isinstance((end_date := parse_date(req, 'end_date')), func.HttpResponse):
        return end_date
    logging.info(f"Requesting data {resolution}, {product}, {start_date}, {end_date}")
    rasters = DATABASE.get_grids_by_resolution_and_dates(
        start_date=start_date,
        end_date=end_date,
        resolution_name=resolution # type: ignore
    )
    
    if rasters is None:
        return create_error_response('resolution', "did not exist in the database", resolution, 400, None)
    grids = [xarray_operations.raster_to_xarray(raster) for raster in rasters]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for grid in grids:
            file_name = str(grid.time.data).split('T')[0]
            zip_file.writestr(f"{file_name}.nc", grid.to_netcdf(None, engine='scipy'))
    return func.HttpResponse(zip_buffer.getvalue(), status_code = 200, headers=GLOBAL_HEADERS)
