from fastapi import FastAPI, Form
from crawler_for_api import Web_Crawler
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router

def include_router(app):
    app.include_router(general_pages_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    return(app)

app = start_application()

"""
@app.get("/")
def welcome():
    return "welcome"" ""world"

@app.get("/greet/{name}")
def greet(name:str):
    return {"welcome":name}
"""

@app.get("/current/destination={destination}/origin={origin}")
def current(destination:str, origin:str):
    return Web_Crawler(destination, origin).clean_up_sections()
