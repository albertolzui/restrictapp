from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, File, UploadFile, Form
#from apis.general_pages.route_restrictions_output import *

templates = Jinja2Templates(directory="templates")
account_login_router = APIRouter()

@account_login_router.get("/account/login")
async def login(request:Request):
    return templates.TemplateResponse("general_pages/account_login.html", {"request":request})

@account_login_router.post("/account/login")
async def login(request:Request):
    return templates.TemplateResponse("general_pages/account_login.html", {"request":request})

@account_login_router.get("/account/changePassword")
async def login_password_update(request:Request):
    return templates.TemplateResponse("general_pages/account_change_password.html", {"request":request})

@account_login_router.post("/account/changePassword")
async def login_password_update(request:Request):
    return templates.TemplateResponse("general_pages/account_change_password.html", {"request":request})