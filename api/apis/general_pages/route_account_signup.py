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
account_signup_router = APIRouter()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP GET API URI calls the asynchronous function "signup" which returns the html page "account_signup.html" (the signup page).

@account_signup_router.get("/account/signup")
async def signup(request:Request):
    return templates.TemplateResponse("general_pages/account_signup.html", {"request":request})


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This HTTP POST API URI calls the asynchronous function also named "signup" which the html page "login_from_signup.html" (where the user is able to log in directly after signing up), 
# along with the variable "message" which is passed into it and varies based on whether or not the user's signup credentials already exist in the database. The signup function here takes 
# the username, password and email from the html form with a post method and passes all to the user_signup() function as defined in the User_man class in user_management.py which checks 
# stores a user's signup credentials into the database only if such credentials don't already exist.

@account_signup_router.post("/account/signup")
async def signup(request:Request, username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    entry = User_man(username, password, email).user_signup()
    if entry == "Insert successful !":
        message = "User Signup was successful"
        return templates.TemplateResponse("general_pages/login_from_signup.html", {"request":request, "message": message})

    elif entry == "User already exists!":
        message = "User already exists, proceed to login or create new user account"
        return templates.TemplateResponse("general_pages/login_from_signup.html", {"request":request, "message": message})
    

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------