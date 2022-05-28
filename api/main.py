from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from crawler_for_api_revised import *
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from apis.general_pages.route_restrictions_output import restriction_output_router
from apis.general_pages.route_account_login import account_login_router
from apis.general_pages.route_account_signup import account_signup_router
from fastapi import FastAPI, Response, File, UploadFile, Form


client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp

def include_router(app):
    app.include_router(general_pages_router)
    app.include_router(restriction_output_router)
    app.include_router(account_login_router)
    app.include_router(account_signup_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    return(app)

app = start_application()

     


"""
@app.get("/current/destination={destination}/origin={origin}")
def current(destination:str, origin:str):
    state = Web_Crawler(destination, origin).currency_check()
    return state["name"]
"""

    
