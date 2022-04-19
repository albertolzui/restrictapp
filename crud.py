from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status
from pymongo import MongoClient
import pymongo

#MongoDB connection info
CONNECTION_STRING =
client = MongoClient()