from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, File, UploadFile, Form
#from apis.general_pages.route_restrictions_output import *

templates = Jinja2Templates(directory="templates")
account_signup_router = APIRouter()

@account_signup_router.get("/account/signup")
async def signup(request:Request):
    return templates.TemplateResponse("general_pages/account_signup.html", {"request":request})

@account_signup_router.post("/account/signup")
async def signup(request:Request):
    return templates.TemplateResponse("general_pages/account_signup.html", {"request":request})
