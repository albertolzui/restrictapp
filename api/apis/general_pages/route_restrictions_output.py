from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crawler_for_api import *

templates = Jinja2Templates(directory="templates")
restriction_output_router = APIRouter()

#This function stores information contained in the database into variables which can be used in the html document titled "restriction_output.html"
# It does this by:
#   - storing what is returned by the currency_check() function as defined in crawler_for_api.py into the variable "state";
#   - storing arrays accessed through their column name in state into variables named after the sections of the page where they would be placed/found
#   - using conditional statements to format each section's output based on the number of indexes of the array, the formatted subsections are then stored in a dictionary
# The function returns all variables that are to be passed to the html file and assigns each one a name through which it can be accessed in the html file.
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

    response_overview = overview_list_to_str
    if "entry_details" in state:
        entry_information = state["entry_details"]
        entry_info = ' '.join(map(str, entry_information[1:]))

    else:
        entry_info = "Entry information not currently available"

    response_country = response_name.title()
    response_country_name = response_country.replace("-", " ")

    outgoing_travel_details = state["outgoing_travel"]

    headings = ["Test type", "Details and exceptions", "Quarantine requirements", "Details and exceptions"]

    outgoing_travel_details.remove("Test type")
    outgoing_travel_details.remove("Details and exceptions")
    outgoing_travel_details.remove("Quarantine requirements")
    outgoing_travel_details.remove("Details and exceptions")

    o_t_d = {
        "line1" : outgoing_travel_details[3] + ":",
        "line2" : ' '.join(map(str, outgoing_travel_details[4:]))
    }

    response_outgoing_travel = outgoing_travel_details
    if len(overview) > 4:
        return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, 
        "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "ov_line3": response_overview["line3"], "ov_line4": response_overview["line4"], 
        "entry_details": entry_info, "outgoing_travel_details": response_outgoing_travel, "o_t_d_line1": o_t_d["line1"], "o_t_d_line2": o_t_d["line2"]})
    elif len(overview) <= 4:
        return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, 
        "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "ov_line3": response_overview["line3"], "entry_details": entry_info, "outgoing_travel_details": response_outgoing_travel, 
        "o_t_d_line1": o_t_d["line1"], "o_t_d_line2": o_t_d["line2"]})


