# Import Requirements:

from operator import index
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crawler_for_api_all_possible_trips import *
from user_management import *

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Templating & Routing

templates = Jinja2Templates(directory="templates")
restriction_output_router = APIRouter()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "restriction_output" which stores information contained in the database into variables which can be used in the html document titled "restriction_output.html"
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


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "restriction_output_logged_in" which stores information contained in the database into variables which can be used in the html document titled "restriction_output_logged_in.html" while a registered user is logged in.
# It does this by:
#   - storing what is returned by the currency_check() function as defined in crawler_for_api.py into the variable "state";
#   - validating the user and fetching the users saved trips through the get_saved_trips() function as defined in the User_man class in user_management.py
#   - comparing the user's saved trips with the trip the user is currently viewing to present an option to save the trip or to inform the user that the trip is already saved
#   - storing arrays accessed through their column name in state into variables named after the sections of the page where they would be placed/found
#   - using conditional statements to format each section's output based on the number of indexes of the array, the formatted subsections are then stored in a dictionary
# The function returns all variables that are to be passed to the html file and assigns each one a name through which it can be accessed in the html file.

@restriction_output_router.get("/restriction-output/destination={destination}/origin={origin}/user={username}")
async def restriction_output_logged_in(request:Request, destination:str, origin:str, username:str):
    state = Web_Crawler_plus(destination, origin.title()).currency_check()   
    user_trips = User_man("albertolz").get_saved_trips()
    if user_trips != "no saved trips" and user_trips != None:
        link_saved = user_trips.get("link")
    save_check = f"https://restrictapp.deta.dev/restriction-output/destination={destination}/origin={origin}/user={username}"
    save_pack = f"https://restrictapp.deta.dev/restriction-output/save/destination={destination}/origin={origin}/user={username}"
    if link_saved == save_check:
        save_packet = "javascript:void(0);"
    else:
        save_packet = save_pack
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

    return templates.TemplateResponse("general_pages/restrictions_output_logged_in.html", {"request":request, "country_name": response_country_name, "ov_mask": other_covid_restrictions["mask"], "ov_rest": other_covid_restrictions["restaurants"], "ov_bars": other_covid_restrictions["bars"],
    "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "entry_details": entry_info, "vacc": vaccination, "test": testing, "quar": quarantine, "user": username, "save_packet": save_packet})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# This HTTP GET API URI calls the asynchronous function "restriction_output_logged_in_save_trip" which stores a user's saved trip information in the database and returns html document titled "restriction_output_logged_in.html along with the variables it requires, it also stores information contained in the database into variables which can be used in the html document titled "restriction_output_logged_in.html" while a registered user is logged in.
# It does this by:
#   - storing what is returned by the currency_check() function as defined in crawler_for_api.py into the variable "state";
#   - validating the user and saving the current trip being viewed which the user tried to save through the user_preferences() function as defined in the User_man class in user_management.py
#   - ensuring the trip won't be "savable" once saved and informing the user that the trip is already saved
#   - storing arrays accessed through their column name in state into variables named after the sections of the page where they would be placed/found
#   - using conditional statements to format each section's output based on the number of indexes of the array, the formatted subsections are then stored in a dictionary
# The function returns all variables that are to be passed to the html file and assigns each one a name through which it can be accessed in the html file.

@restriction_output_router.get("/restriction-output/save/destination={destination}/origin={origin}/user={username}")
async def restriction_output_logged_in_save_trip(request:Request, destination:str, origin:str, username:str):
    state = Web_Crawler_plus(destination, origin.title()).currency_check()
    link = f"https://restrictapp.deta.dev/restriction-output/destination={destination}/origin={origin}/user={username}"
    save_packet = "javascript:void(0);"
    save_packet_unpacked = User_man(username).user_preferences(origin, destination, link)
    save_packet_unpacked
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

    return templates.TemplateResponse("general_pages/restrictions_output_logged_in.html", {"request":request, "country_name": response_country_name, "ov_mask": other_covid_restrictions["mask"], "ov_rest": other_covid_restrictions["restaurants"], "ov_bars": other_covid_restrictions["bars"],
    "ov_line1": response_overview["line1"], "ov_line2": response_overview["line2"], "entry_details": entry_info, "vacc": vaccination, "test": testing, "quar": quarantine, "user": username, "save_packet": save_packet})

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------