from operator import index
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crawler_for_api_revised import *

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
    
    response_other_covid_restrictions = state["overview"]

    other_covid_restrictions = {
        "mask": response_other_covid_restrictions[22],
        "restaurants": response_other_covid_restrictions[18],
        "bars": response_other_covid_restrictions[20],
    }
    response_name = state["name"]
    overview = state["overview"]
    overview_list_to_str = {
        "line1" : overview[1],
        "line2" : overview[9] + overview[10], 
        }
    
    response_overview = overview_list_to_str
    if "entry_details" in state:
        entry_information = state["entry_details"]
        del entry_information[-1]
        del entry_information[-1]
        entry_info = ' '.join(map(str, entry_information[1:]))

    else:
        entry_info = "Entry information not currently available"

    response_country = response_name.title()
    response_country_name = response_country.replace("-", " ")

    vaccination = state["vaccination"]
    testing = state["testing"]
    quarantine = state["quarantine"]
    lock = quarantine.index(f"Do I need to wear a mask in {response_country_name}?")
    del quarantine[lock:]

    vacc = {
        "line1" : vaccination[1] + vaccination[2],
        "line2" : vaccination[3] + vaccination[4],
    }

    test = {
        "line1" : ' '.join(map(str, testing[1:]))
    }

    quar = {
        "line1" : ' '.join(map(str, quarantine[1:]))
    }

    return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, "ov_mask": other_covid_restrictions["mask"], "ov_rest": other_covid_restrictions["restaurants"], "ov_bars": other_covid_restrictions["bars"],
    "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "entry_details": entry_info, "vacc_line1": vacc["line1"], "vacc_line2": vacc["line2"], "test": test["line1"], "quar_line1": quar["line1"]})



