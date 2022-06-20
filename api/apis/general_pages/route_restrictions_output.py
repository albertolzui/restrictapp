from operator import index
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crawler_for_api_revised import *
from crawler_for_api_all_possible_trips import *

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
    state = Web_Crawler_plus(destination, origin.title()).currency_check()   
    overview = state["overview"]
    other_covid_restrictions = {
        "mask": state["masks"],
        "restaurants": state["restaurants"],
        "bars": state["bars"],
    }
    response_name = state["name"]
    if overview[10] == "Entry":
        overview_list_to_str = {
            "line1" : overview[1],
            "line2" : overview[9], 
            }
    else:
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

    
    if "vaccination" in state:
        vac_info = state["vaccination"]
        bow = vac_info.index(f"Can I travel to {response_country_name} if I am vaccinated?")
        del vac_info[bow:]
        vaccination = ' '.join(map(str, vac_info[1:]))
    else:
        vaccination = "Information on vaccination requirements not currently available"

    if "testing" in state:
        test_info = state["testing"]
        testing = ' '.join(map(str, test_info[1:]))
    else:
        testing = "Information on travel test requirements not currently available"

    if "quarantine" in state:
        quar = state["quarantine"]
        lock = quar.index(f"Do I need to wear a mask in {response_country_name}?")
        del quar[lock:]
        quarantine = ' '.join(map(str, quar[1:]))
    else:
        quarantine = "Information on quarantine requirements not currently available"

    return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, "ov_mask": other_covid_restrictions["mask"], "ov_rest": other_covid_restrictions["restaurants"], "ov_bars": other_covid_restrictions["bars"],
    "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "entry_details": entry_info, "vacc": vaccination, "test": testing, "quar": quarantine})



