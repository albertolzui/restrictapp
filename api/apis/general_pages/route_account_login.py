from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, File, UploadFile, Form
from user_management import *
#from apis.general_pages.route_restrictions_output import *

templates = Jinja2Templates(directory="templates")
account_login_router = APIRouter()

@account_login_router.get("/account/login")
async def login(request:Request):
    return templates.TemplateResponse("general_pages/account_login.html", {"request":request})

@account_login_router.post("/account/login")
async def login(request:Request, username: str = Form(...), password: str = Form(...)):
    validate = User_man(username, password).user_login()
    if validate:
        status = "successful"
    else:
        status = "failed"

    if status == "successful":
        return templates.TemplateResponse("general_pages/user_dashboard.html", {"request":request, "user":username})
    else:
        return templates.TemplateResponse("general_pages/login_failed.html", {"request":request})

@account_login_router.get("/account/changePassword")
async def login_password_update(request:Request):
    return templates.TemplateResponse("general_pages/account_change_password.html", {"request":request})

@account_login_router.post("/account/changePassword")
async def login_password_update(request:Request):
    return templates.TemplateResponse("general_pages/account_change_password.html", {"request":request})