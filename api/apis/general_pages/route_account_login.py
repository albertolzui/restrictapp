# Import Requirements:

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, File, UploadFile, Form
from user_management import *

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Templating & Routing

templates = Jinja2Templates(directory="templates")
account_login_router = APIRouter()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "login" which returns the html page "account_login.html" (the login page).

@account_login_router.get("/account/login")
async def login(request:Request):
    return templates.TemplateResponse("general_pages/account_login.html", {"request":request})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP POST API URI calls the asynchronous function also named "login" which returns a list of country names stored in the variable "countries" 
# as well as the html page "login_failed.html" or "user_dashbord.html" depending on whether or not a user's login attempt was successful. The function
# employs the user_login() function as defined in the User_man class in user_nanagement.py to validate a user's login credentials. When a user's 
# log in credentials fail validation, the login_failed.html page is returned, prompting the user to verify their credentials. A successful log in 
# attempt triggers another function - get_saved_trips() as defined in the User_man class in user_management.py which fetches information about a 
# user's saved trips, if information exists on saved trips, details of the trip are passed into user_dashboard.html, otherwise a corresponding 
# message & details set is passed to user_dashboard.html along with the user's username.

@account_login_router.post("/account/login")
async def login(request:Request, username:str = Form(...), password:str = Form(...)):
    countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'British-Virgin-Islands', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape-Verde', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech-Republic', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'East-Timor', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Federated-States-of-Micronesia', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory-Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Korea', 'North-Macedonia', 'Northern-Mariana-Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 'Republic-of-the-Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Korea', 'South-Sudan', 'Spain', 'Sri-Lanka', 'St-Maarten', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The-Bahamas', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-States', 'Uruguay', 'U-S-Virgin-Islands', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
    validate = User_man(username, password).user_login()
    if validate == None:
        return templates.TemplateResponse("general_pages/login_failed.html", {"request":request})    
    elif "username" in validate:
        saved = User_man(username).get_saved_trips()
        if saved == None or saved == "no saved trips":
            saved_trips = ["No trip saved yet"]
            src = "404" 
            dest = "404" 
            link = "javascript:void(0);" 
            msg = "No trips found"
        else:
            saved_trips = saved
            src = saved_trips["origin"]
            dest = saved_trips["destination"]
            link = saved_trips["link"]
            msg = f"Travel from {src.title()} to {dest.title()}"
        return templates.TemplateResponse("general_pages/user_dashboard.html", {"request":request, "user":username, "countries": countries, "src": src, "dest": dest, "link": link, "msg": msg})

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "delete_trip" which triggers the function delete_saved_trip() as defined in the 
# User_man class in user_management.py which deletes a users saved trip using the user's username, destination and origin of the trip to
# be deleted. After which the function get_saved_trips() is called as defined in the User_man class in user_management.py which fetches 
# information about a user's saved trips, if information exists on saved trips, details of the trip are passed into user_dashboard.html, 
# otherwise a corresponding message & details set is passed to user_dashboard.html along with the user's username. In the end the page
# user_dashboard.html is returned.


@account_login_router.get("/{username}/trip/delete/{origin}-to-{destination}")
async def delete_trip(request:Request, username: str, origin: str, destination: str):
    status = User_man(username).delete_saved_trips(origin, destination)
    if status == "no saved trips":
        msg = "no saved trips"
    else:
        if status == "Update successful !":
            msg = "Trip deleted"

    saved = User_man(username).get_saved_trips()
    if saved == None or saved == "no saved trips":
        saved_trips = ["No trip saved yet"]
        src = "404" 
        dest = "404" 
        link = "javascript:void(0);" 
        msg = "No trips found"
    else:
        saved_trips = saved
        src = saved_trips["origin"]
        dest = saved_trips["destination"]
        link = saved_trips["link"]
        msg = f"Travel from {src.title()} to {dest.title()}"

    return templates.TemplateResponse("general_pages/user_dashboard.html", {"request":request, "user":username, "saved_trips":saved_trips, "src": src, "dest": dest, "link": link, "msg": msg})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "account_delete" which returns the html page "del_confirmation.html" (where the 
# user confirms deletion of their account).

@account_login_router.get("/account/delete")
async def account_delete(request:Request):
    return templates.TemplateResponse("general_pages/del_confirmation.html", {"request":request})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP POST API URI calls the asynchronous function also named "account_delete" which collects the user's credentials as form inputs 
# and passes them to the delete_user_account() function as defined in the User_man class in user_management.py which deletes a user's 
# account information in its entirety from the  database.

@account_login_router.post("/account/delete")
async def account_delete(request:Request, username: str = Form(...), password: str = Form(...)):
    get_rid = User_man(username, password).delete_user_account()
    if get_rid == "Delete successful !":
        message = " "
        return templates.TemplateResponse("general_pages/homepage.html", {"request":request, "message":message})
    else:
        message = "Account deletion was unsuccessful, ensure details are correct and try again"
        return templates.TemplateResponse("general_pages/del_confirmation.html", {"request":request, "message": message})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "login_password_update" which returns the html page "account_change_password.html" 
# (where the user is able to initiate a password change on their account information stored in the database.

@account_login_router.get("/account/changePassword")
async def login_password_update(request:Request):
    return templates.TemplateResponse("general_pages/account_change_password.html", {"request":request})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET route calls the asynchronous function "rtd" which returns a list of country names stored in the variable "countries" as well
# as the html page "user_dashboard.html". It also fetches information on the user's previously saved trips using the get_saved_trips() 
# function as defined in the User_man class in user_management.py which is passed into the html page.

@account_login_router.get("/account/rtd/{username}")
async def rtd(request:Request, username:str):
    countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'British-Virgin-Islands', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape-Verde', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech-Republic', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'East-Timor', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Federated-States-of-Micronesia', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory-Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Korea', 'North-Macedonia', 'Northern-Mariana-Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 'Republic-of-the-Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Korea', 'South-Sudan', 'Spain', 'Sri-Lanka', 'St-Maarten', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The-Bahamas', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-States', 'Uruguay', 'U-S-Virgin-Islands', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 'Zimbabwe']    
    saved = User_man(username).get_saved_trips()
    if saved == None or saved == "no saved trips":
        saved_trips = ["No trip saved yet"]
        src = "404" 
        dest = "404" 
        link = "javascript:void(0);" 
        msg = "No trips found"
    else:
        saved_trips = saved
        src = saved_trips["origin"]
        dest = saved_trips["destination"]
        link = saved_trips["link"]
        msg = f"Travel from {src.title()} to {dest.title()}"



    return templates.TemplateResponse("general_pages/user_dashboard.html", {"request":request, "user":username, "countries": countries, "src": src, "dest": dest, "link": link, "msg": msg})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
