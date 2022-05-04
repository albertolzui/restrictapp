import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *

client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp

destination = input("destination?").lower()
origin = "DE"

class Web_Crawler:
    def __init__(self, destination, origin):
        self.destination = destination
        self.origin = origin
        self.country = destination.capitalize()
        self.headings = [f"{self.country} Travel Restrictions", f"{self.country} entry details and exceptions", f"Outgoing travel to {self.country}", "Return travel",
         f"Other COVID-19 restrictions for {self.country}", "Additional resources"]
        

    def page_lister(self):
        ori= "origin="+origin
        url = 'https://www.kayak.com/travel-restrictions/'+ destination + '?' + ori
        r = requests.get(url)
        src = r.content
        soup = BeautifulSoup(src, 'html.parser')
        all_text_on_page = soup.get_text("|")
        page = list(all_text_on_page.split("|"))
        return page

    # This function returns a list of indexes by searching a list (search_list) to see if it contains an element 
    # (search_item)from another list, and subsequently returning the corresponding index in search_list; 
    def find_indices(self, search_list, search_item):
        indices = []
        for (index, item) in enumerate(search_list):
            if item == search_item:
                indices.append(index)

        return indices

    # This function takes the list of complete text from the webpage(page), and the list it will be compared to(headings).
    # Then it calls the find_indices function and takes the returned list and appends the contents of the elements and appends it into a new list(save_index)
    # Said list will be returned
    def get_text_from_index(self, page):
        headings = self.headings
        page = self.page_lister()
        i = 0
        save_index = []
        while i < len(headings):     
            index = self.find_indices(page, headings[i])
            bootleg = index[0]
            save_index.append(bootleg)
            i = i + 1

        return save_index
    

    # This function needs two parameters: first is the list returned by the get_text_from_index() function, and the list derived from all text on the webpage.
    # It then returns a list containing sublists which hold different page sections distinguished by the specified indexes in header_index.

    def sections_into_list(self):
        headings = self.headings
        header_index = self.get_text_from_index(headings)
        page = self.page_lister()
        put_into_db = []
        i = 0
        while i < len(header_index):
            if i+1 < len(header_index):
                put_into_db.append(page[header_index[i]:header_index[i+1]])
            else:
                put_into_db.append(page[header_index[i]:])
            i = i + 1
        return put_into_db    
    

#print(Web_Crawler(destination, origin).sections_into_list())
    def clean_up_sections(self):
        cleaned_list = []
        dirty_list = self.sections_into_list()
        for i in range(len(dirty_list)):
            conveyor = str(dirty_list[i])
            first_clean = conveyor.replace("', '", " ")
            cleaned_list.append(first_clean)
        return cleaned_list

      
    def crawl_into_db(self):
        payload = self.clean_up_sections()

        overview = payload[0]
        entry_details = payload[1]
        outgoing_travel = payload[2]
        return_travel = payload[3]
        other_covid_restrictions = payload[4]
        additional_resources = payload[5]

        destination_log = {"name": self.destination, "overview": overview, "entry_details": entry_details, "outgoing_travel": outgoing_travel, "return_travel": return_travel, "other_covid_restrictions": other_covid_restrictions, "additional_resources": additional_resources, "date": datetime.datetime.utcnow()}        
        update = db.country_restrictions.insert_one(destination_log)
        return update

