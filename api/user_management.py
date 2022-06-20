import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *


client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp


class User_man:
    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email

    def user_signup(self):
        preferences = []
        find_user_with = {"username": self.username, "password": self.password}
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

    def user_preferences(self, new_preferences):
        find_user_with = {"username": self.username, "password": self.password}
        cull = db.user.find_one(find_user_with, {'_id': 0})
        preferences = list(cull["preferences"])
        updated_preferences = preferences.append(new_preferences)
        preference_set = {"$set":  {"preferences": updated_preferences, "date": datetime.datetime.utcnow()}}        
        update = db.update.update_one(find_user_with, preference_set)
        if update:
            return "Update successful !"

    def user_password(self, new_password):
        find_user_with = {"username": self.username, "email": self.email}
        update_password_and_time = {"$set":  {"password": new_password, "date": datetime.datetime.utcnow()}}        
        update = db.update.update_one(find_user_with, update_password_and_time)
        if update:
            return "Update successful !"


