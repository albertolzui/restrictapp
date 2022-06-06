import requests
from bs4 import BeautifulSoup 
import datetime
from pymongo import MongoClient
from cred_albert import *
from crawler_for_api_revised import *
from crawler_for_api_all_possible_trips import *

countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 
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

origins = ['AF', 'AL', 'DZ', 'AS', 'AO', 'AI', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BA', 'BW', 'BR', 'BN', 'BG',
 'BF', 'BI', 'CV', 'KH', 'CM', 'CA', 'BQ', 'KY', 'CF', 'TD', 'CL', 'CN', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'HR', 'CU', 'CW', 'CY', 'CZ', 'CI', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG',
 'SV', 'GQ', 'ER', 'EE', 'SZ', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GN', 'GW', 'GY', 'HT', 'HN', 
 'HK', 'HU', 'IS', 'IN', 'ID', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'XK', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 
 'MO', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 
 'MK', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'PR', 'QA', 'RO', 'RU', 'RW', 'RE', 'BL', 'KN', 'LC', 'MF', 'VC', 'WS', 'ST', 'SA', 'SN', 'RS', 
 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'SS', 'ES', 'LK', 'SD', 'SR', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 
 'UG', 'UA', 'AE', 'GB', 'US', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW']

#triad = dict(zip(origins, countries))
#print(triad)
country_code = {
    'AF': 'Afghanistan', 'AL': 'Albania', 'DZ': 'Algeria', 'AS': 'American-Samoa', 'AO': 'Angola', 'AI': 'Anguilla', 'AG': 'Antigua-and-Barbuda', 'AR': 'Argentina', 'AM': 'Armenia', 
    'AW': 'Aruba', 'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaijan', 'BS': 'The-Bahamas', 'BH': 'Bahrain', 'BD': 'Bangladesh', 'BB': 'Barbados', 'BY': 'Belarus', 'BE': 'Belgium', 
    'BZ': 'Belize', 'BJ': 'Benin', 'BM': 'Bermuda', 'BT': 'Bhutan', 'BO': 'Bolivia', 'BA': 'Bosnia-and-Herzegovina', 'BW': 'Botswana', 'BR': 'Brazil', 'BN': 'Brunei-Darussalam', 
    'BG': 'Bulgaria', 'BF': 'Burkina-Faso', 'BI': 'Burundi', 'CV': 'Cape-Verde', 'KH': 'Cambodia',  'CM': 'Cameroon', 'CA': 'Canada', 'BQ': 'Caribbean-Netherlands', 'KY': 'Cayman-Islands', 
    'CF': 'Central-African-Republic', 'TD': 'Chad', 'CL': 'Chile', 'CN': 'China', 'CO': 'Colombia', 'KM': 'Comoros', 'CG': 'Democratic-Republic-of-the-Congo', 
    'CD': 'Republic-of-the-Congo', 'CK': 'Cook-Islands', 'CR': 'Costa-Rica', 'HR': 'Croatia', 'CU': 'Cuba', 'CW': 'Curacao', 'CY': 'Cyprus', 'CZ': 'Czech-Republic', 'CI': 'Ivory-Coast', 
    'DK': 'Denmark', 'DJ': 'Djibouti', 'DM': 'Dominica', 'DO': 'Dominican-Republic', 'EC': 'Ecuador', 'EG': 'Egypt', 'SV': 'El-Salvador', 'GQ': 'Equatorial-Guinea', 'ER': 'Eritrea', 
    'EE': 'Estonia', 'SZ': 'Eswatini', 'ET': 'Ethiopia', 'FK': 'Falkland-Islands-Islas-Malvinas', 'FO': 'Faroe-Islands', 'FJ': 'Fiji', 'FI': 'Finland', 'FR': 'France', 
    'GF': 'French-Guiana', 'PF': 'French-Polynesia', 'GA': 'Gabon', 'GM': 'Gambia', 'GE': 'Georgia', 'DE': 'Germany', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GR': 'Greece', 'GL': 'Greenland', 
    'GD': 'Grenada', 'GP': 'Guadeloupe', 'GU': 'Guam', 'GT': 'Guatemala', 'GN': 'Guinea', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HT': 'Haiti', 'HN': 'Honduras', 'HK': 'Hong-Kong', 
    'HU': 'Hungary', 'IS': 'Iceland', 'IN': 'India', 'ID': 'Indonesia', 'IQ': 'Iraq', 'IE': 'Ireland', 'IL': 'Israel', 'IT': 'Italy', 'JM': 'Jamaica', 'JP': 'Japan', 'JE': 'Jersey', 
    'JO': 'Jordan', 'KZ': 'Kazakhstan', 'KE': 'Kenya', 'KI': 'Kiribati', 'XK': 'Kosovo', 'KP': 'North-Korea', 'KR': 'South-Korea', 'KW': 'Kuwait', 'KG': 'Kyrgyzstan', 'LA': 'Laos', 
    'LV': 'Latvia', 'LB': 'Lebanon', 'LS': 'Lesotho', 'LR': 'Liberia', 'LY': 'Libya', 'LI': 'Liechtenstein', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'MO': 'Macau', 'MG': 'Madagascar', 
    'MW': 'Malawi', 'MY': 'Malaysia', 'MV': 'Maldives', 'ML': 'Mali', 'MT': 'Malta', 'MH': 'Marshall-Islands', 'MQ': 'Martinique', 'MR': 'Mauritania', 'MU': 'Mauritius', 'YT': 'Mayotte', 
    'MX': 'Mexico', 'FM': 'Federated-States-of-Micronesia', 'MD': 'Moldova', 'MN': 'Mongolia', 'ME': 'Montenegro', 'MS': 'Montserrat', 'MA': 'Morocco', 'MZ': 'Mozambique', 'MM': 'Myanmar', 
    'NA': 'Namibia', 'NR': 'Nauru', 'NP': 'Nepal', 'NL': 'Netherlands', 'NC': 'New-Caledonia', 'NZ': 'New-Zealand', 'NI': 'Nicaragua', 'NE': 'Niger', 'NG': 'Nigeria', 'MK': 'North-Macedonia',
    'MP': 'Northern-Mariana-Islands', 'NO': 'Norway', 'OM': 'Oman', 'PK': 'Pakistan', 'PW': 'Palau', 'PS': 'Palestinian-Territories', 'PA': 'Panama', 'PG': 'Papua-New-Guinea', 
    'PY': 'Paraguay', 'PE': 'Peru', 'PH': 'Philippines', 'PL': 'Poland', 'PT': 'Portugal', 'PR': 'Puerto-Rico', 'QA': 'Qatar', 'RO': 'Romania', 'RU': 'Russia', 'RW': 'Rwanda', 'RE': 'Reunion', 
    'BL': 'Saint-Barthelemy', 'KN': 'Saint-Kitts-and-Nevis', 'LC': 'Saint-Lucia', 'MF': 'Saint-Martin', 'VC': 'Saint-Vincent-and-the-Grenadines', 'WS': 'Samoa', 
    'ST': 'Sao-Tome-and-Principe', 'SA': 'Saudi-Arabia', 'SN': 'Senegal', 'RS': 'Serbia', 'SC': 'Seychelles', 'SL': 'Sierra-Leone', 'SG': 'Singapore', 'SX': 'St-Maarten', 'SK': 'Slovakia', 
    'SI': 'Slovenia', 'SB': 'Solomon-Islands', 'SO': 'Somalia', 'ZA': 'South-Africa', 'SS': 'South-Sudan', 'ES': 'Spain', 'LK': 'Sri-Lanka', 'SD': 'Sudan', 'SR': 'Suriname', 'SE': 'Sweden', 
    'CH': 'Switzerland', 'SY': 'Syria', 'TW': 'Taiwan', 'TJ': 'Tajikistan', 'TZ': 'Tanzania', 'TH': 'Thailand', 'TL': 'East-Timor', 'TG': 'Togo', 'TO': 'Tonga', 'TT': 'Trinidad-and-Tobago', 
    'TN': 'Tunisia', 'TR': 'Turkey', 'TM': 'Turkmenistan', 'TC': 'Turks-and-Caicos-Islands', 'TV': 'Tuvalu', 'UG': 'Uganda', 'UA': 'Ukraine', 'AE': 'United-Arab-Emirates', 
    'GB': 'United-Kingdom', 'US': 'United-States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 'VU': 'Vanuatu', 'VE': 'Venezuela', 'VN': 'Vietnam', 'VG': 'British-Virgin-Islands', 
    'VI': 'U-S-Virgin-Islands', 'WF': 'Wallis-and-Futuna', 'EH': 'Western-Sahara', 'YE': 'Yemen', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'}

#book_not = triad.keys()
#book_it = triad.values()

#print(book_it)
#print(book_not)


# Germany to all possible destinations
"""
l = len(countries)
i = 1
for country in countries:
    base = country.lower()
    print(f"{country} : {base}")
    state = Web_Crawler(base, "DE").currency_check()
    print(f"{country} entry was successful!... ... ... ... ... ... ... ... ... ... ... ... ... ... ...  {i} of {l}")
    i = i + 1
"""

#___________________________________________________________________________________________________________________________________________________________


# All possible trips:

l = len(countries)
i = 1
for origin in origins:
    for country in countries:
        base = country.lower()
        print(f"{country} : {base}")
        state = Web_Crawler_plus(base, origin).currency_check()
        if state:
            print(f"{origin} to {country} entry was successful!... ... ... ... ... ... ... ... ... ... ... ... ... ... ...  {i} of {l * l}")
        i = i + 1
#    print(f" All possible destinations from {origin} have been covered, moving on to next possible origin")
#"""


    

#clay = Web_Crawler("british-virgin-islands", "DE").get_text_from_index(Web_Crawler("british-virgin-islands", "DE").page_lister()) 
#print(clay)
#print(len(countries))
#"""

#doo = Web_Crawler_plus("nigeria", "AF").cull_from_db()
#print(doo)