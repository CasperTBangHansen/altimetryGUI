import azure.functions as func
from shared_src import GLOBAL_HEADERS, xarray_operations
import logging
from typing import Optional
from datetime import datetime, date
from shared_src.HandleInput import create_error_response
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

def main(req: func.HttpRequest) -> func.HttpResponse:
    rasters = DATABASE.get_grids_by_resolution(resolution_name='Neighbors=100, kernel=linear')
    if rasters is None:
        return create_error_response('resolution', "did not exist in the database", 'Neighbors=100, kernel=linear', 400, None)
        return func.HttpResponse(json.dumps({'status': "ERROR"}), status_code = 400, headers=GLOBAL_HEADERS)
    grids = [xarray_operations.raster_to_xarray(raster) for raster in rasters]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for grid in grids:
            file_name = str(grid.time.data).split('T')[0]
            zip_file.writestr(f"{file_name}.nc", grid.to_netcdf(None))
    return func.HttpResponse(json.dumps({'status': "success"}), status_code = 200, headers=GLOBAL_HEADERS)
