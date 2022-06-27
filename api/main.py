from logging import exception
from fastapi.staticfiles import StaticFiles
from crawler_for_api_revised import *
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from apis.general_pages.route_restrictions_output import restriction_output_router
from apis.general_pages.route_account_login import account_login_router
from apis.general_pages.route_account_signup import account_signup_router
from fastapi import FastAPI, Response, File, UploadFile, Form, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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





@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    if item_id == 4:
        raise HTTPException(status_code=404, detail="Uff! This is rather embarassing, but what you're looking for does not exist - yet!. Please check back at a later date. - Restrictapp Team")
    return {"item_id": item_id}    

     


"""
@app.get("/current/destination={destination}/origin={origin}")
def current(destination:str, origin:str):
    state = Web_Crawler(destination, origin).currency_check()
    return state["name"]
"""

    
