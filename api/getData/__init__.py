# import logging
# from typing import Optional
# from datetime import datetime, date
import azure.functions as func
# from ..shared_src.databases import database, tables
status = None
import_status = "v1 "
try:
    from ..shared_src.HandleInput import parse_input, create_error_response, status
    import_status += "Relative"
except:
    try:
        from api.shared_src.HandleInput import parse_input, create_error_response, status
        import_status += "Abs1"
    except:
        try:
            from altimetryGUI.api.shared_src.HandleInput import parse_input, create_error_response, status
            import_status += "Abs2"
        except:
            try:
                from shared_src.HandleInput import parse_input, create_error_response, status
                import_status += "Abs3"
            except:
                import_status += "FAILED"
import_status += f" {status}"


# from os import environ
import json

# Logging
# logging.getLogger(__name__)

# Database
# database = database.Database(
#     username=environ["ALTIMETRY_USERNAME"],
#     password=environ["ALTIMETRY_PASSWORD"],
#     host=environ["ALTIMETRY_HOST"],
#     port=environ["ALTIMETRY_DATABASE_PORT"],
#     database_name=environ["ALTIMETRY_DATABASE"],
#     engine=environ["ALTIMETRY_DATABASE_CONNECTION_ENGINE"],
#     database_type=environ["ALTIMETRY_DATABASE_TYPE"],
#     create_tables=environ["ALTIMETRY_CREATE_TABLES"] == 'true'
# )

# def getData(start_date: date, end_date: date):
#     """Access data and return"""
#     logging.info("Requesting data from the blob stroage")
#     logging.info(f"Data interval is {start_date} - {end_date}")
#     return "BLAA"

# def handle_input(date_str: Optional[str], placeholder: date) -> date | None:
#     """
#     Format a date string format to datetime
#     or use the placeholder if date_str is None
#     """
#     if date_str is None:
#         return placeholder
#     try:
#         # Cast to datetime
#         return datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError or TypeError:
#         return None

def main(req: func.HttpRequest) -> func.HttpResponse:
    # logging.info('Requesting data using the getData endpoint')
    
    # Get start and end date
    # from_date = parse_input(req, 'from')
    # to_date = parse_input(req, 'to')
    # start_date = handle_input(from_date, datetime.strptime("1991-08-03","%Y-%m-%d").date())
    # end_date = handle_input(to_date, datetime.now().date())
    
    # Check dates
    # for date, field, param in zip([start_date, end_date], ['from', 'to'], [from_date, to_date]):
        # if date is None:
            # return create_error_response(field, "has an invalid format", param, 400, "%Y-%m-%d")
        
    # Request data from the blob storage
    # data = getData(start_date=start_date, end_date=end_date) # type: ignore

    # Return data
    return func.HttpResponse(json.dumps({"status": import_status}))
