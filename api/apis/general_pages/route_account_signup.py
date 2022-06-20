from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, File, UploadFile, Form

from user_management import *
#from apis.general_pages.route_restrictions_output import *

templates = Jinja2Templates(directory="templates")
account_signup_router = APIRouter()

@account_signup_router.get("/account/signup")
async def signup(request:Request):
    return templates.TemplateResponse("general_pages/account_signup.html", {"request":request})

@account_signup_router.post("/account/signup")
async def signup(request:Request, username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    entry = User_man(username, password, email).user_signup()
    if entry == "Insert successful !":
        message = "User Signup was successful"
        return templates.TemplateResponse("general_pages/login_from_signup.html", {"request":request, "message": message})

    elif entry == "User already exists!":
        message = "User already exists, proceed to login or create new user account"
        return templates.TemplateResponse("general_pages/login_from_signup.html", {"request":request, "message": message})
    
