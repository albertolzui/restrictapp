import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *
import random

client = MongoClient("mongodb+srv://" + user + ":" + key + "@restrictapp-one.sb8jy.mongodb.net/Restrictapp?retryWrites=true&w=majority")
db = client.Restrictapp


class Empfehler:
    def __init__(self, mask_output, bar_output, res_output, origin):
        self.countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 
        'The-Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 
        'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cape-Verde', 'Cambodia', 'Cameroon', 'Canada', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 
        'Chile', 'China', 'Colombia', 'Comoros', 'Democratic-Republic-of-the-Congo', 'Republic-of-the-Congo', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 
        'Czech-Republic', 'Ivory-Coast', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 
        'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 
        'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 
        'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'North-Korea', 'South-Korea', 'Kuwait', 
        'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 
        'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Federated-States-of-Micronesia', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 
        'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Macedonia', 'Northern-Mariana-Islands', 
        'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 
        'Romania', 'Russia', 'Rwanda', 'Reunion', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 
        'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'St-Maarten', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 
        'South-Africa', 'South-Sudan', 'Spain', 'Sri-Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'East-Timor', 'Togo', 
        'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 
        'United-States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'British-Virgin-Islands', 'U-S-Virgin-Islands', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 
        'Zimbabwe']

        self.mask_output = mask_output
        self.bar_output = bar_output
        self.res_output = res_output
        self.origin = origin
        self.all_filter_queries = self.mask_output + self.bar_output + self.res_output
        find_entry_switch = {
            "mandatoryopenopen": {
                "overview": f"{self.origin}",
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open', 'Open with restrictions']}, 
                "restaurants": {"$in" : ['Open', 'Open with restrictions']} },
            "mandatoryopenowr" : {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "mandatoryopenclosed": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "mandatoryowropen": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open']} },
            "mandatoryowrowr": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "mandatoryowrclosed": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "mandatoryclosedopen": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open']} },
            "mandatoryclosedowr": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "mandatoryclosedclosed": {
                "masks": {"$in" : ['Required in enclosed environments.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },

            "mandatory-or-recommendedopenopen": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open']} },
            "mandatory-or-recommendedopenowr" : {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "mandatory-or-recommendedopenclosed": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "mandatory-or-recommendedowropen": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open']} },
            "mandatory-or-recommendedowrowr": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "mandatory-or-recommendedowrclosed": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "mandatory-or-recommendedclosedopen": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open']} },
            "mandatory-or-recommendedclosedowr": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "mandatory-or-recommendedclosedclosed": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            
            "recommendedopenopen": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open']} },
            "recommendedopenowr" : {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "recommendedopenclosed": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "recommendedowropen": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open']} },
            "recommendedowrowr": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "recommendedowrclosed": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "recommendedclosedopen": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open']} },
            "recommendedclosedowr": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "recommendedclosedclosed": {
                "masks": {"$in" : ['Recommended in enclosed environments and public transportation.', 'Recommended in public spaces.']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },


            "not-requiredopenopen": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open']} },
            "not-requiredopenowr" : {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "not-requiredopenclosed": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "not-requiredowropen": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open']} },
            "not-requiredowrowr": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "not-requiredowrclosed": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Open with restrictions']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },
            "not-requiredclosedopen": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open']} },
            "not-requiredclosedowr": {
                "masks": {"$in" : ['Required in public spaces and enclosed environments.', 'Required in public spaces and public transportation.', 'Recommended in enclosed environments and public transportation.', 'Required in public spaces, enclosed environments and public transportation.', 'Required in enclosed environments.','Recommended in public spaces.', 'Required on public transportation.', 'Required in enclosed environments and public transportation.', 'Required in public spaces.', 'Required in public spaces, enclosed environments and public transportation']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Open with restrictions']} },
            "not-requiredclosedclosed": {
                "masks": {"$in" : ['Not required in public spaces and enclosed environments.', 'Not required in public spaces and public transportation.', 'Not required in public spaces, enclosed environments and public transportation', 'Not required in public spaces.', 'Not required in enclosed environments.', 'Not required on public transportation.', 'Not required in enclosed environments and public transportation.']}, 
                "bars": {"$in" : ['Information on restaurant access is currently unavailable']}, 
                "restaurants": {"$in" : ['Information on restaurant access is currently unavailable']} },                        
        }
        if self.all_filter_queries in find_entry_switch:
            self.use_this_query = find_entry_switch.get(self.all_filter_queries)        
    def oracle_picks(self):
        find_entry_from = {"masks": self.mask_output, "bars": self.bar_output, "restaurants": self.res_output}
        if self.mask_output == "egal" and self.bar_output == "egal" and self.res_output == "egal":
            random_seven = random.sample(self.countries, 20)
            return random_seven

        else:
            cull = db.all_possible_trips.find(self.use_this_query, {'_id': 0}).limit(20)
            if cull:
                empfehlungen = []
                for doc in cull:
#                    land = cull["name"]
                    empfehlungen.append(doc)
                hold = []
                for dict in empfehlungen:
                    land = dict.get("name")
                    hold.append(land)
                länder = list(set(hold))
                länder.sort()

                return länder        