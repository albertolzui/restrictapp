import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *

client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp

#destination = input("destination?").lower()
#origin = "DE"

class Web_Crawler:
    def __init__(self, destination, origin):
        self.destination = str(destination)
        self.origin = origin
        self.country = self.destination.title()
        self.country_name = self.country.replace("-", " ")
        countries_that_take_a_definite_article = ["Gambia", "Czech Republic"]
        countries_that_take_a_definite_article_and_have_alt_headings = ["Comoros"]
        if self.country_name in countries_that_take_a_definite_article:
            self.headings = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Outgoing travel to the {self.country_name}", "Return travel",
            f"Other COVID-19 restrictions for the {self.country_name}", "Additional resources"]
        else:
            self.headings = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Outgoing travel to {self.country_name}", "Return travel", 
            f"Other COVID-19 restrictions for {self.country_name}", "Additional resources"]
        
        if self.country_name in countries_that_take_a_definite_article_and_have_alt_headings:
            self.alt_headings = [f"{self.country_name} Travel Restrictions", f"Outgoing travel to the {self.country_name}", "Return travel", 
            f"Other COVID-19 restrictions for the {self.country_name}", "Additional resources"] 
        else:
            self.alt_headings = [f"{self.country_name} Travel Restrictions", f"Outgoing travel to {self.country_name}", "Return travel", 
            f"Other COVID-19 restrictions for {self.country_name}", "Additional resources"] 

    def page_lister(self):
        ori= "origin="+self.origin
        url = 'https://www.kayak.com/travel-restrictions/'+ self.destination + '?' + ori
        r = requests.get(url)
        src = r.content
        soup = BeautifulSoup(src, 'html.parser')
        all_text_on_page = soup.get_text("|")
        page = list(all_text_on_page.split("|"))
        return page

    def link_lister(self):
        ori= "origin="+self.origin
        url = 'https://www.kayak.com/travel-restrictions/'+ self.destination + '?' + ori
        r = requests.get(url)
        src = r.content
        soup = BeautifulSoup(src, 'html.parser')
        links = soup.find_all("a")
        linkie = []
        for link in links:
            linkie.append(link.get('href'))  
        linked = linkie[8:]
        del linked[-1]
    #    for child in a_tag.children:
    #        title.append(child)        
        return linked


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
        if f"{self.country_name} entry details and exceptions" in page:
            headings = self.headings
            i = 0
            save_index = []
            while i < len(headings):     
                index = self.find_indices(page, headings[i])
                bootleg = index[0]
                save_index.append(bootleg)
                i = i + 1

            return save_index
        else:
            headings = self.alt_headings
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
        page = self.page_lister()
        if f"{self.country_name} entry details and exceptions" in page:
            headings = self.headings
            header_index = self.get_text_from_index(headings)
            put_into_db = []
            i = 0
            while i < len(header_index):
                if i+1 < len(header_index):
                    put_into_db.append(page[header_index[i]:header_index[i+1]])
                else:
                    put_into_db.append(page[header_index[i]:])
                i = i + 1
            return put_into_db             
        else:
            headings = self.alt_headings
            header_index = self.get_text_from_index(headings)
            put_into_db = []
            i = 0
            while i < len(header_index):
                if i+1 < len(header_index):
                    put_into_db.append(page[header_index[i]:header_index[i+1]])
                else:
                    put_into_db.append(page[header_index[i]:])
                i = i + 1
            return put_into_db    
    

# This functions takes the list "put_into_db" generated by the "sections_into_list" function and removes the excess commas and apostrophes
    def clean_up_sections(self):
        cleaned_list = []
        dirty_list = self.sections_into_list()
        for i in range(len(dirty_list)):
            conveyor = str(dirty_list[i])
            first_clean = conveyor.replace("', '", " ")
            cleaned_list.append(first_clean)
        return dirty_list


# This function writes the "cleaned_list" generated by the "clean_up_sections" function into the database
    def crawl_into_db(self):
        page = self.page_lister()
        payload = self.clean_up_sections()
        links_payload = self.link_lister()
        if f"{self.country_name} entry details and exceptions" in page:
            overview = payload[0]
            entry_details = payload[1]
            outgoing_travel = payload[2]
            return_travel = payload[3]
            other_covid_restrictions = payload[4]
            additional_resources = payload[5]

            destination_log = {"name": self.destination, "overview": overview, "entry_details": entry_details, "outgoing_travel": outgoing_travel, "return_travel": return_travel, "other_covid_restrictions": other_covid_restrictions, "additional_resources": additional_resources, "relevant_links": links_payload, "date": datetime.datetime.utcnow()}        
            insert = db.country_restrictions.insert_one(destination_log)
            if insert:
                return "Insert successful !"
        else:
            overview = payload[0]
            outgoing_travel = payload[1]
            return_travel = payload[2]
            other_covid_restrictions = payload[3]
            additional_resources = payload[4]

            destination_log = {"name": self.destination, "overview": overview, "outgoing_travel": outgoing_travel, "return_travel": return_travel, "other_covid_restrictions": other_covid_restrictions, "additional_resources": additional_resources, "relevant_links": links_payload, "date": datetime.datetime.utcnow()}        
            insert = db.country_restrictions.insert_one(destination_log)
            if insert:
                return "Insert successful !"

# This function finds the first entry in the database where the "name" is the same as the destination input
    def cull_from_db(self):
        find_entry_where = {"name": self.destination}
        cull = db.country_restrictions.find_one(find_entry_where, {'_id': 0})
        if cull:
            return cull

# This function updates the first entry in the database where the "name" is the same as the destination input
    def update_db_entry(self):
        payload = self.clean_up_sections()

        overview = payload[0]
        entry_details = payload[1]
        outgoing_travel = payload[2]
        return_travel = payload[3]
        other_covid_restrictions = payload[4]
        additional_resources = payload[5]

        search_query = {"name": self.destination}
        new_destination_log = {"$set": {"name": self.destination, "overview": overview, "entry_details": entry_details, "outgoing_travel": outgoing_travel, "return_travel": return_travel, "other_covid_restrictions": other_covid_restrictions, "additional_resources": additional_resources, "date": datetime.datetime.utcnow()}}        
        update = db.country_restrictions.update_one(search_query, new_destination_log)
        if update:
            return "Update successful !"

# This function deletes the first entry in the database where the "name" is the same as the destination input
    def delete_entry(self):
        delete_entry_where = {"name": self.destination}
        delete = db.country_restrictions.delete_one(delete_entry_where)
        if delete:
            return "Delete successful !"



# This function finds the first entry in the database where the "name" is the same as the destination input, if it exists; 
# the function checks to see if it is not more than 48 hours old, if it isn't the function returns the entry; if the entry is older 
# than 48 hours it is deleted and a newly crawled version of the deleted entry is written into the database and then returned. If 
# the entry did not exist at all at the first attempt, then it is crawled and written into the database from where it is returned.
    def currency_check(self):
        check = self.cull_from_db()
        if check:
            entry_date = check["date"]
            max_age_of_info = datetime.timedelta(days = 1)
            time_now = datetime.datetime.utcnow()
            duration_of_info = time_now - entry_date
            if duration_of_info < max_age_of_info:
                return check
            else:
                self.delete_entry()
                self.crawl_into_db()
                check = self.cull_from_db()
                return check
        else:
            self.crawl_into_db()
            check = self.cull_from_db()
            if check:
                entry_date = check["date"]
                max_age_of_info = datetime.timedelta(days = 1)
                time_now = datetime.datetime.utcnow()
                duration_of_info = time_now - entry_date
                if duration_of_info < max_age_of_info:
                    return check


