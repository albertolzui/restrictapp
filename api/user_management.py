# Import Requirements:

import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv
from cred import *


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# MongoDB Connection Credentials:

load_dotenv(find_dotenv())

USER = os.environ.get("USER")
KEY = os.environ.get("KEY")
client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# The User_man Class: 
# (See notes on the User_man Class in testing.py along with a sample call you can make)

class User_man:
    def __init__(self, username, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email



    def user_signup(self):
        preferences = []
        find_user_with = {
            "username": { "$in" : [self.username]}, 
            "email": {"$in" : [self.email]} }
        cull = db.user.find_one(find_user_with, {'_id': 0})
        if cull:
            return "User already exists!"
        else:
            user_log = {"username": self.username, "password": self.password, "email": self.email, "preferences": preferences, "date": datetime.datetime.utcnow()}        
            insert = db.user.insert_one(user_log)
            if insert:
                return "Insert successful !"



    def user_login(self):
        user_check = {"username": self.username, "password": self.password}        
        cull = db.user.find_one(user_check, {'_id': 0})
        if cull:
            return cull



    def user_preferences(self, origin, destination, link):
        find_user_with = {"username": self.username}
        cull = db.user.find_one(find_user_with, {'_id': 0})

        new_entry = {}
        new_entry["origin"] = origin
        new_entry["destination"] = destination
        new_entry["link"] = link

        preference_set = {"$set":  {"preferences": new_entry, "date": datetime.datetime.utcnow()}}        
        update = db.user.update_one(find_user_with, preference_set)
        if update:
            return "Update successful !"



    def get_saved_trips(self):
        find_user_with = {"username": self.username}
        cull = db.user.find_one(find_user_with, {'_id': 0})
        preferences = cull["preferences"]

        if preferences:
            if preferences == " ":
                return "no saved trips"
            else:
                return preferences
        else:
            return None



    def delete_saved_trips(self, origin, destination):
        find_user_with = {"username": self.username}
        cull = db.user.find_one(find_user_with, {'_id': 0})
        preferences = cull["preferences"]
        if preferences == None or preferences == " ":
            return "no saved trips"
        if preferences.get("origin") == origin and preferences.get("destination") == destination:
                poof = " "
                preference_set = {"$set":  {"preferences": poof, "date": datetime.datetime.utcnow()}}        
                update = db.user.update_one(find_user_with, preference_set)
                if update:
                    return "Update successful !"



    def delete_user_account(self):
        delete_entry_where = {"username": self.username, "password": self.password}
        delete = db.user.delete_one(delete_entry_where)
        if delete:
            return "Delete successful !"    



    def user_password(self, new_password):
        find_user_with = {"username": self.username, "email": self.email}
        update_password_and_time = {"$set":  {"password": new_password, "date": datetime.datetime.utcnow()}}        
        update = db.user.update_one(find_user_with, update_password_and_time)
        if update:
            return "Update successful !"


