from fastapi import FastAPI, Request
from crawler_for_api import Web_Crawler

app = FastAPI()


@app.get("/")
def welcome():
    return "welcome"" ""world"

@app.get("/greet/{name}")
def greet(name:str):
    return {"welcome":name}

@app.get("/current/destination={destination}/origin={origin}")
def current(destination:str, origin:str):
    return Web_Crawler(destination, origin).clean_up_sections()
