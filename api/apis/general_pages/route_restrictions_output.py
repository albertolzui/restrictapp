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
    relevant_links = state["relevant_links"]
    clean_rel_links = []
    for link in relevant_links:
        if link.find(".html"):
            new_link = link.replace("https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html", "https://www.rki.de/DE/Home/homepage_node")
            clean_rel_links.append(new_link)

    response_other_covid_restrictions = state["other_covid_restrictions"]
    if response_other_covid_restrictions:
        if len(response_other_covid_restrictions) <= 5:
                other_covid_restrictions = {
                    "mask": response_other_covid_restrictions[3],
                    "restaurants": ' --- ',
                    "bars": ' --- ',
                }
        elif len(response_other_covid_restrictions) > 5 and len(response_other_covid_restrictions) <= 6:
                other_covid_restrictions = {
                    "mask": response_other_covid_restrictions[3],
                    "restaurants": response_other_covid_restrictions[5],
                    "bars": ' --- ',
                }
        elif len(response_other_covid_restrictions) >= 8:
            other_covid_restrictions = {
                "mask": response_other_covid_restrictions[3],
                "restaurants": response_other_covid_restrictions[5],
                "bars": response_other_covid_restrictions[7],
            }
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
    return_travel_details = state["return_travel"]

    headings = ["Test type", "Details and exceptions", "Quarantine requirements", "Details and exceptions"]
    
    for i in headings:
        if i in outgoing_travel_details:
            outgoing_travel_details.remove(i)
        if i in return_travel_details:
            return_travel_details.remove(i)

    o_t_d = {
        "line1" : outgoing_travel_details[3] + ":",
        "line2" : ' '.join(map(str, outgoing_travel_details[4:]))
    }

    r_t_d = {
        "line1" : return_travel_details[3] + ":",
        "line2" : ' '.join(map(str, return_travel_details[4:]))
    }



    if len(overview) > 4:
        return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, "ov_mask": other_covid_restrictions["mask"], "ov_rest": other_covid_restrictions["restaurants"], "ov_bars": other_covid_restrictions["bars"],
        "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "ov_line3": response_overview["line3"], "ov_line4": response_overview["line4"], 
        "entry_details": entry_info, "o_t_d_line1": o_t_d["line1"], "o_t_d_line2": o_t_d["line2"], "r_t_d_line1": r_t_d["line1"], "r_t_d_line2": r_t_d["line2"], "rel_links": clean_rel_links})
    elif len(overview) <= 4:
        return templates.TemplateResponse("general_pages/restriction_output.html", {"request":request, "country_name": response_country_name, "ov_mask": other_covid_restrictions["mask"], "ov_rest": other_covid_restrictions["restaurants"], "ov_bars": other_covid_restrictions["bars"],
        "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "ov_line3": response_overview["line3"], "entry_details": entry_info, 
        "o_t_d_line1": o_t_d["line1"], "o_t_d_line2": o_t_d["line2"], "r_t_d_line1": r_t_d["line1"], "r_t_d_line2": r_t_d["line2"], "rel_links": clean_rel_links})



