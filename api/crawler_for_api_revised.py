import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *

client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp



class Web_Crawler:
    def __init__(self, destination, origin):
        self.destination = str(destination)
        self.origin = origin
        self.country = self.destination.title()
        self.country_name_and = self.country.replace("And", "and")
        self.country_name_of = self.country_name_and.replace("Of", "of")
        self.country_name_the = self.country_name_of.replace("The", "the")
        self.country_name = self.country_name_the.replace("-", " ")
        complex_name_format = {
            "Antigua and Barbuda": "Antigua And Barbuda",
            "Curacao": "Curaçao",
            "Falkland Islands Islas Malvinas": "Falkland Islands (Islas Malvinas)",
            "Guinea Bissau": "Guinea-Bissau",
            "Reunion": "Réunion",
            "Saint Barthelemy": "Saint Barthélemy",
            "Sao Tome and Principe": "São Tomé and Príncipe",
            "St Maarten": "St. Maarten",
            "the Bahamas": "The Bahamas",
            "U S Virgin Islands": "U.S. Virgin Islands"
        }
        if self.country_name in complex_name_format:
            self.country_name = complex_name_format.get(self.country_name)

        countries_that_take_a_definite_article = ["Gambia", "Czech Republic", "British Virgin Islands", "Caribbean Netherlands", "Cayman Islands", 
        "Central African Republic", "Cook Islands", "Democratic Republic of the Congo", "Dominican Republic", "Faroe Islands", "Maldives", 
        "Marshall Islands", "Netherlands", "Northern Mariana Islands", "Philippines", "Solomon Islands", "Turks and Caicos Islands", 'United Arab Emirates', 
        'United States', 'United Kingdom', 'U.S. Virgin Islands'] 
        countries_that_take_a_definite_article_and_have_alt_headings = ["Comoros", "Caribbean Netherlands", "Central African Republic", "Cook Islands", "Marshall Islands"]
        if self.country_name in countries_that_take_a_definite_article:
            self.headings = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", "Documents & Additional resources", f"Can I travel to the {self.country_name} from Germany?", f"Do I need a COVID test to enter the {self.country_name}?", 
            f"Can I travel to the {self.country_name} without quarantine?"]
            self.minus_doc = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Can I travel to the {self.country_name} from Germany?", f"Do I need a COVID test to enter the {self.country_name}?", 
            f"Can I travel to the {self.country_name} without quarantine?"]
            self.minus_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", "Documents & Additional resources", f"Can I travel to the {self.country_name} from Germany?"]
        else:
            self.headings = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", "Documents & Additional resources", f"Can I travel to {self.country_name} from Germany?", f"Do I need a COVID test to enter {self.country_name}?", 
            f"Can I travel to {self.country_name} without quarantine?"]
            self.minus_doc = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Can I travel to {self.country_name} from Germany?", f"Do I need a COVID test to enter {self.country_name}?", 
            f"Can I travel to {self.country_name} without quarantine?"]
            self.minus_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", "Documents & Additional resources", f"Can I travel to {self.country_name} from Germany?"]
            self.minus_doc_and_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Can I travel to {self.country_name} from Germany?"]
        
        
        if self.country_name in countries_that_take_a_definite_article_and_have_alt_headings:
            self.alt_headings = [f"{self.country_name} Travel Restrictions", "Documents & Additional resources", f"Can I travel to the {self.country_name} from Germany?", f"Do I need a COVID test to enter the {self.country_name}?", 
            f"Can I travel to the {self.country_name} without quarantine?"]
            self.minus_ede_and_doc = [f"{self.country_name} Travel Restrictions", f"Can I travel to the {self.country_name} from Germany?", f"Do I need a COVID test to enter the {self.country_name}?", 
            f"Can I travel to the {self.country_name} without quarantine?"]
            self.minus_ede_and_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", "Documents & Additional resources", f"Can I travel to the {self.country_name} from Germany?"]
            self.minus_doc_and_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Can I travel to the {self.country_name} from Germany?"]
        else:
            self.alt_headings = [f"{self.country_name} Travel Restrictions", "Documents & Additional resources", f"Can I travel to {self.country_name} from Germany?", f"Do I need a COVID test to enter {self.country_name}?", 
            f"Can I travel to {self.country_name} without quarantine?"]
            self.minus_ede_and_doc = [f"{self.country_name} Travel Restrictions", f"Can I travel to {self.country_name} from Germany?", f"Do I need a COVID test to enter {self.country_name}?", f"Can I travel to {self.country_name} without quarantine?"]
            self.minus_ede_doc_and_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", f"Can I travel to {self.country_name} from Germany?"]
            self.minus_doc_and_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", f"{self.country_name} entry details and exceptions", f"Can I travel to {self.country_name} from Germany?"]
            self.minus_ede_and_test_question_and_quar_q = [f"{self.country_name} Travel Restrictions", "Documents & Additional resources", f"Can I travel to {self.country_name} from Germany?"]



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
        page = self.page_lister()
        dork = "Documents & Additional resources"
        if f"{self.country_name} entry details and exceptions" in page:
            if dork in page:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.headings
                else:
                    headings = self.minus_test_question_and_quar_q
            else:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.minus_doc
                else:
                    headings = self.minus_doc_and_test_question_and_quar_q
            i = 0
            save_index = []
            while i < len(headings):     
                index = self.find_indices(page, headings[i])
                bootleg = index[0]
                save_index.append(bootleg)
                i = i + 1

            return save_index
        else:
            if "Documents & Additional resources" in page:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.alt_headings
                else:
                    headings = self.minus_ede_and_test_question_and_quar_q
            else:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.minus_ede_and_doc
                else:
                    headings = self.minus_ede_doc_and_test_question_and_quar_q
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
        dork = "Documents & Additional resources"
        if f"{self.country_name} entry details and exceptions" in page:
            if dork in page:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.headings
                else:
                    headings = self.minus_test_question_and_quar_q
            else:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.minus_doc
                else:
                    headings = self.minus_doc_and_test_question_and_quar_q
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
            if "Documents & Additional resources" in page:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.alt_headings
                else:
                    headings = self.minus_ede_and_test_question_and_quar_q
            else:
                if f"Do I need a COVID test to enter {self.country_name}?" in page or f"Do I need a COVID test to enter the {self.country_name}?" in page:
                    headings = self.minus_ede_and_doc
                else:
                    headings = self.minus_ede_doc_and_test_question_and_quar_q
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
        dork = "Documents & Additional resources"
        countries_with_incomplete_faq = ['American Samoa', 'Bhutan', 'Brunei Darussalam', 'Cameroon', 'China', 'Cook Islands', 
        'East Timor', 'Eswatini', 'Falkland Islands (Islas Malvinas)', 'Federated States of Micronesia', 'French Guiana', 'Hong Kong', 
        'Kiribati', 'Lesotho', 'Libya', 'Macau', 'Marshall Islands', 'Mayotte', 'Montserrat', 'Nauru', 'North Korea', 'Samoa', 'Syria', 
        'Taiwan', 'Tonga', 'Turkmenistan', 'Tuvalu', 'Vanuatu', 'Wallis and Futuna', 'Western Sahara', 'Yemen']
        if f"{self.country_name} entry details and exceptions" in page:
            if dork in page:
                if self.country_name in countries_with_incomplete_faq:
                    overview = payload[0]
                    entry_details = payload[1]
                    vaccination = payload[3]
                else:
                    overview = payload[0]
                    entry_details = payload[1]
                    vaccination = payload[3]
                    testing = payload[4]
                    quarantine = payload[5]
            else:
                if self.country_name in countries_with_incomplete_faq:
                    overview = payload[0]
                    entry_details = payload[1]
                    vaccination = payload[2]
                else:
                    overview = payload[0]
                    entry_details = payload[1]
                    vaccination = payload[2]
                    testing = payload[3]
                    quarantine = payload[4]

            if self.country_name in countries_with_incomplete_faq:
                destination_log = {"name": self.destination, "overview": overview, "entry_details": entry_details, "vaccination": vaccination, "date": datetime.datetime.utcnow()}        
            else:
                destination_log = {"name": self.destination, "overview": overview, "entry_details": entry_details, "vaccination": vaccination, "testing": testing, "quarantine": quarantine, "date": datetime.datetime.utcnow()}        
            insert = db.country_restrictions.insert_one(destination_log)
            if insert:
                return "Insert successful !"
        else:
            if dork in page:
                if self.country_name in countries_with_incomplete_faq:
                    overview = payload[0]
                    vaccination = payload[2]
                else:
                    overview = payload[0]
                    vaccination = payload[2]
                    testing = payload[3]
                    quarantine = payload[4]
            else:
                if self.country_name in countries_with_incomplete_faq:
                    overview = payload[0]
                    vaccination = payload[1]
                else:
                    overview = payload[0]
                    vaccination = payload[1]
                    testing = payload[2]
                    quarantine = payload[3]

            if self.country_name in countries_with_incomplete_faq:
                destination_log =  {"name": self.destination, "overview": overview,"vaccination": vaccination, "date": datetime.datetime.utcnow()}        
            else:
                destination_log =  {"name": self.destination, "overview": overview,"vaccination": vaccination, "testing": testing, "quarantine": quarantine, "date": datetime.datetime.utcnow()}        
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
        page = self.page_lister()
        payload = self.clean_up_sections()
        search_query = {"name": self.destination}

        if f"{self.country_name} entry details and exceptions" in page:
            overview = payload[0]
            entry_details = payload[1]
            vaccination = payload[3]
            testing = payload[4]
            quarantine = payload[5]
            new_destination_log = {"$set":  {"name": self.destination, "overview": overview, "entry_details": entry_details, "vaccination": vaccination, "testing": testing, "quarantine": quarantine, "date": datetime.datetime.utcnow()}}        
        else:
            overview = payload[0]
            vaccination = payload[2]
            testing = payload[3]
            quarantine = payload[4]
            new_destination_log = {"$set":  {"name": self.destination, "overview": overview, "vaccination": vaccination, "testing": testing, "quarantine": quarantine, "date": datetime.datetime.utcnow()}}        
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


