from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    return {"welcome":"world"}

@app.get("/greet/{name}")
def greet(name:str):
    return {"welcome":name}
