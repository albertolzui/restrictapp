#from pymongo import MongoClient
#from cred_albert import *
from web_scrapper import Trip_Advisor

#client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")

#print(client.list_database_names())

#db = client.Restrictapp
#print(db.list_collection_names())


destination = input("destination? ")
origin = input("origin ?")

#Trip_Advisor(destination, origin).crawl_into_db()
current_trip = Trip_Advisor(destination, origin)
row_input = current_trip.trip_info()
print(row_input[14])
