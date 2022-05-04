from fastapi import FastAPI
from fastapi.responses import FileResponse

home_path = "../index.html"
app = FastAPI()

@app.get("/")
def welcome():
    return {"welcome":"world"}

@app.get("/greet/{name}")
def greet(name:str):
    return {"welcome":name}

@app.get("/home", response_class=FileResponse)
async def main():
    return home_path