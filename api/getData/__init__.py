import logging
from datetime import datetime
import azure.functions as func

def getData(start_date: datetime.date, end_date: datetime.date):
    """Access data and return"""
    logging.info("Getting data")
    logging.info(f"Data interval is {start_date} - {end_date}")
    data = [1,2,3,4]
    return data

def handle_input(input: str, placeholder: datetime.date):
    """Handle the input formatting"""
    if not input:
        input = placeholder
    else:
        try:
            input = datetime.strptime(input,"%Y-%m-%d").date()
        except ValueError or TypeError:
            return func.HttpResponse("Enter start and end date in format yyyy-mm-dd")
    return input

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start_date = req.params.get('from')
    end_date = req.params.get('to')
    
    start_date = handle_input(start_date, datetime.strptime("1991-08-03","%Y-%m-%d").date())
    end_date = handle_input(end_date, datetime.now().date())
    data = getData(start_date=start_date, end_date=end_date)
    return func.HttpResponse(f"{data}")


    
