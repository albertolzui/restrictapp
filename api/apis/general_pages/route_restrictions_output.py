from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crawler_for_api import *

templates = Jinja2Templates(directory="templates")
restriction_output_router = APIRouter()

@restriction_output_router.get("/restriction-output/destination={destination}/origin={origin}")
async def restriction_output(request:Request, destination:str, origin:str):
    state = Web_Crawler(destination, origin).currency_check()
    response_name = state["name"]
    overview = state["overview"]
    overview_list_to_str = ' '.join(map(str, overview[1:]))
    if len(overview) >= 5:
        overview1 = overview[0] + ":"
        overview2 = overview[1] + " - " + overview[2] + "."
        overview3 = overview[3] + overview[4]
        overview_list_to_str = {
            "line1" : overview1,
            "line2" : overview2, 
            "line3" : overview3,
            "line4" : ' '.join(map(str, overview[5:]))
        }
    elif len(overview) <= 4:
        overview1 = overview[0] + ":"
        overview2 = overview[1] + " - " + overview[2] + "."
        overview3 = overview[3]
        overview_list_to_str = {
            "line1" : overview1,
            "line2" : overview2, 
            "line3" : overview3,
        }
    #resp_overview = overview
    #response_overview = resp_overview[2]
    response_overview = overview_list_to_str
    if "entry_details" in state:
        entry_information = state["entry_details"]
        entry_info = ' '.join(map(str, entry_information[1:]))
    #    entry_details = entry_info.split("exceptions", 1)[1]
    else:
        entry_info = "Entry information not currently available"

    response_country = response_name.title()
    response_country_name = response_country.replace("-", " ")
    if len(overview) > 4:
        return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, 
        "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "ov_line3": response_overview["line3"], "ov_line4": response_overview["line4"], 
        "entry_details": entry_info})
    elif len(overview) <= 4:
        return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, 
        "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "ov_line3": response_overview["line3"], "entry_details": entry_info})


