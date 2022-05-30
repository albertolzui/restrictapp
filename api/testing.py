import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *
from crawler_for_api_revised import *

"""
#from crawler_for_api import *
from crawler_for_api_revised import *


#state = Web_Crawler("thailand", "DE").link_lister()
#del state[0:24]
#boil = " ".join()

relevant_links = ["relevant_links", "bay", "boo", "na", "coo", "clo", "doe", "porr", "ppw", "ppow"]
lines = ["line1", "line2", "line3", "line4", "line5", "line6", "line7", "line8", "line9", "line10", "line11", "line12"]
dict = {}
for i,j in relevant_links, lines:
    while i < len(relevant_links):
        while j < len(lines):
            if relevant_links.index(i) == lines.index(j):
                dict[j] = i
                j = j + 1
    i = i + 1


#Web_Crawler("thailand", "DE").get_text_from_index()

#print(Web_Crawler("czech-republic", "DE").cull_from_db())
#print(Web_Crawler("south-africa", "DE").country_name)
#if "Belaru Travel Restrictions" in co:
#    print("True")
#else:
#page = Web_Crawler("nigeria", "DE").page_lister() 
#del page[0:24]
#state = Web_Crawler("nigeria", "DE").get_text_from_index(page)
#print(state)
#duck = Web_Crawler("nigeria", "DE").find_indices(page, " Can I travel to Nigeria from Germany?")
#print(duck[0])
clay = Web_Crawler("thailand", "DE").page_lister() 
print(clay)

r = requests.get("https://travelbans.org/africa/ghana/")
src = r.content
soup = BeautifulSoup(src, 'html.parser')
all_text_on_page = soup.get_text("|")
page = list(all_text_on_page.split("|"))
print(page)
"""
countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'British-Virgin-Islands', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape-Verde', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech-Republic', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'East-Timor', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Federated-States-of-Micronesia', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory-Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Korea', 'North-Macedonia', 'Northern-Mariana-Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 'Republic-of-the-Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Korea', 'South-Sudan', 'Spain', 'Sri-Lanka', 'St-Maarten', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The-Bahamas', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-States', 'Uruguay', 'U-S-Virgin-Islands', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
l = len(countries)
i = 1
for country in countries:
    base = country.lower()
    print(f"{country} : {base}")
    state = Web_Crawler(base, "DE").currency_check()
    print(f"{country} entry was successful!. {i} of {l}")
    i = i + 1
"""
clay = Web_Crawler("british-virgin-islands", "DE").get_text_from_index(Web_Crawler("british-virgin-islands", "DE").page_lister()) 
print(clay)
#print(len(countries))
#"""