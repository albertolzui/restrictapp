from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, File, UploadFile, Form
from empfehler import *
from user_management import *


templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()

@general_pages_router.get("/")
async def home(request:Request):
    countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'British-Virgin-Islands', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape-Verde', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech-Republic', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'East-Timor', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Federated-States-of-Micronesia', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory-Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Korea', 'North-Macedonia', 'Northern-Mariana-Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 'Republic-of-the-Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Korea', 'South-Sudan', 'Spain', 'Sri-Lanka', 'St-Maarten', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The-Bahamas', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-States', 'Uruguay', 'U-S-Virgin-Islands', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 'Zimbabwe']

    return templates.TemplateResponse("general_pages/homepage.html", {"request":request, "countries":countries })

@general_pages_router.get("/enquiries")
async def enquiries(request:Request):
    return templates.TemplateResponse("general_pages/enquiries.html", {"request":request})

@general_pages_router.get("/restriction-output/all-possible-destinations-with-mask={mask_output}/bar={bar_output}/restaurant={res_output}/from-origin={origin_country}")
async def homelist(request:Request, mask_output:str, bar_output:str, res_output:str, origin_country:str):
    country_code = {
        'Afghanistan': 'AF', 'Albania': 'AL', 'Algeria': 'DZ', 'American-Samoa': 'AS', 'Angola': 'AO', 'Anguilla': 'AI', 'Antigua-and-Barbuda': 'AG', 'Argentina': 'AR', 'Armenia': 'AM', 
        'Aruba': 'AW', 'Australia': 'AU', 'Austria': 'AT', 'Azerbaijan': 'AZ', 'The-Bahamas': 'BS', 'Bahrain': 'BH', 'Bangladesh': 'BD', 'Barbados': 'BB', 'Belarus': 'BY', 'Belgium': 'BE', 
        'Belize': 'BZ', 'Benin': 'BJ', 'Bermuda': 'BM', 'Bhutan': 'BT', 'Bolivia': 'BO', 'Bosnia-and-Herzegovina': 'BA', 'Botswana': 'BW', 'Brazil': 'BR', 'Brunei-Darussalam': 'BN', 
        'Bulgaria': 'BG', 'Burkina-Faso': 'BF', 'Burundi': 'BI', 'Cape-Verde': 'CV', 'Cambodia': 'KH', 'Cameroon': 'CM', 'Canada': 'CA', 'Caribbean-Netherlands': 'BQ', 
        'Cayman-Islands': 'KY', 'Central-African-Republic': 'CF', 'Chad': 'TD', 'Chile': 'CL', 'China': 'CN', 'Colombia': 'CO', 'Comoros': 'KM', 'Democratic-Republic-of-the-Congo': 'CD', 
        'Republic-of-the-Congo': 'CG', 'Cook-Islands': 'CK', 'Costa-Rica': 'CR', 'Croatia': 'HR', 'Cuba': 'CU', 'Curacao': 'CW', 'Cyprus': 'CY', 'Czech-Republic': 'CZ', 'Ivory-Coast': 'CI', 
        'Denmark': 'DK', 'Djibouti': 'DJ', 'Dominica': 'DM', 'Dominican-Republic': 'DO', 'Ecuador': 'EC', 'Egypt': 'EG', 'El-Salvador': 'SV', 'Equatorial-Guinea': 'GQ', 'Eritrea': 'ER', 
        'Estonia': 'EE', 'Eswatini': 'SZ', 'Ethiopia': 'ET', 'Falkland-Islands-Islas-Malvinas': 'FK', 'Faroe-Islands': 'FO', 'Fiji': 'FJ', 'Finland': 'FI', 'France': 'FR', 
        'French-Guiana': 'GF', 'French-Polynesia': 'PF', 'Gabon': 'GA', 'Gambia': 'GM', 'Georgia': 'GE', 'Germany': 'DE', 'Ghana': 'GH', 'Gibraltar': 'GI', 'Greece': 'GR', 
        'Greenland': 'GL', 'Grenada': 'GD', 'Guadeloupe': 'GP', 'Guam': 'GU', 'Guatemala': 'GT', 'Guinea': 'GN', 'Guinea-Bissau': 'GW', 'Guyana': 'GY', 'Haiti': 'HT', 'Honduras': 'HN', 
        'Hong-Kong': 'HK', 'Hungary': 'HU', 'Iceland': 'IS', 'India': 'IN', 'Indonesia': 'ID', 'Iraq': 'IQ', 'Ireland': 'IE', 'Israel': 'IL', 'Italy': 'IT', 'Jamaica': 'JM', 'Japan': 'JP', 
        'Jersey': 'JE', 'Jordan': 'JO', 'Kazakhstan': 'KZ', 'Kenya': 'KE', 'Kiribati': 'KI', 'Kosovo': 'XK', 'North-Korea': 'KP', 'South-Korea': 'KR', 'Kuwait': 'KW', 'Kyrgyzstan': 'KG', 
        'Laos': 'LA', 'Latvia': 'LV', 'Lebanon': 'LB', 'Lesotho': 'LS', 'Liberia': 'LR', 'Libya': 'LY', 'Liechtenstein': 'LI', 'Lithuania': 'LT', 'Luxembourg': 'LU', 'Macau': 'MO', 
        'Madagascar': 'MG', 'Malawi': 'MW', 'Malaysia': 'MY', 'Maldives': 'MV', 'Mali': 'ML', 'Malta': 'MT', 'Marshall-Islands': 'MH', 'Martinique': 'MQ', 'Mauritania': 'MR', 
        'Mauritius': 'MU', 'Mayotte': 'YT', 'Mexico': 'MX', 'Federated-States-of-Micronesia': 'FM', 'Moldova': 'MD', 'Mongolia': 'MN', 'Montenegro': 'ME', 'Montserrat': 'MS', 'Morocco': 
        'MA', 'Mozambique': 'MZ', 'Myanmar': 'MM', 'Namibia': 'NA', 'Nauru': 'NR', 'Nepal': 'NP', 'Netherlands': 'NL', 'New-Caledonia': 'NC', 'New-Zealand': 'NZ', 'Nicaragua': 'NI', 
        'Niger': 'NE', 'Nigeria': 'NG', 'North-Macedonia': 'MK', 'Northern-Mariana-Islands': 'MP', 'Norway': 'NO', 'Oman': 'OM', 'Pakistan': 'PK', 'Palau': 'PW', 
        'Palestinian-Territories': 'PS', 'Panama': 'PA', 'Papua-New-Guinea': 'PG', 'Paraguay': 'PY', 'Peru': 'PE', 'Philippines': 'PH', 'Poland': 'PL', 'Portugal': 'PT', 
        'Puerto-Rico': 'PR', 'Qatar': 'QA', 'Romania': 'RO', 'Russia': 'RU', 'Rwanda': 'RW', 'Reunion': 'RE', 'Saint-Barthelemy': 'BL', 'Saint-Kitts-and-Nevis': 'KN', 'Saint-Lucia': 'LC', 
        'Saint-Martin': 'MF', 'Saint-Vincent-and-the-Grenadines': 'VC', 'Samoa': 'WS', 'Sao-Tome-and-Principe': 'ST', 'Saudi-Arabia': 'SA', 'Senegal': 'SN', 'Serbia': 'RS', 
        'Seychelles': 'SC', 'Sierra-Leone': 'SL', 'Singapore': 'SG', 'St-Maarten': 'SX', 'Slovakia': 'SK', 'Slovenia': 'SI', 'Solomon-Islands': 'SB', 'Somalia': 'SO', 'South-Africa': 'ZA', 
        'South-Sudan': 'SS', 'Spain': 'ES', 'Sri-Lanka': 'LK', 'Sudan': 'SD', 'Suriname': 'SR', 'Sweden': 'SE', 'Switzerland': 'CH', 'Syria': 'SY', 'Taiwan': 'TW', 'Tajikistan': 'TJ', 
        'Tanzania': 'TZ', 'Thailand': 'TH', 'East-Timor': 'TL', 'Togo': 'TG', 'Tonga': 'TO', 'Trinidad-and-Tobago': 'TT', 'Tunisia': 'TN', 'Turkey': 'TR', 'Turkmenistan': 'TM', 
        'Turks-and-Caicos-Islands': 'TC', 'Tuvalu': 'TV', 'Uganda': 'UG', 'Ukraine': 'UA', 'United-Arab-Emirates': 'AE', 'United-Kingdom': 'GB', 'United-States': 'US', 'Uruguay': 'UY', 
        'Uzbekistan': 'UZ', 'Vanuatu': 'VU', 'Venezuela': 'VE', 'Vietnam': 'VN', 'British-Virgin-Islands': 'VG', 'U-S-Virgin-Islands': 'VI', 'Wallis-and-Futuna': 'WF', 
        'Western-Sahara': 'EH', 'Yemen': 'YE', 'Zambia': 'ZM', 'Zimbabwe': 'ZW'}

    countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'British-Virgin-Islands', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape-Verde', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech-Republic', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'East-Timor', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Federated-States-of-Micronesia', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory-Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Korea', 'North-Macedonia', 'Northern-Mariana-Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 'Republic-of-the-Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Korea', 'South-Sudan', 'Spain', 'Sri-Lanka', 'St-Maarten', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The-Bahamas', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-States', 'Uruguay', 'U-S-Virgin-Islands', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
    länder = Empfehler(mask_output, bar_output, res_output, origin_country).oracle_picks()
    if länder == []:
        n_a = ["Sorry, but there are no results based on your selections"]
        return templates.TemplateResponse("general_pages/homepage.html", {"request":request, "countries":countries, "länder": n_a, "origin_country": origin_country, "origin_sel": origin_country, "mask_sel": mask_output, "bar_sel": bar_output, "res_sel": res_output})    
    else:

        flags = []
        brain = list(länder)
        for land in brain:
            broth = str(land)
            bent = broth.title()
            if bent in country_code:
                code_to_land = country_code.get(bent)
                flag_str = str(code_to_land)
                flag = flag_str.lower()
            flags.append(flag)

        src = []
        for item in flags:
            im = f"{item}.svg"
            src.append(im)

        return templates.TemplateResponse("general_pages/homepage.html", {"request":request, "countries":countries, "länder": länder, "flags": flags, "source": src, "origin_country": origin_country , "origin_sel": origin_country, "mask_sel": mask_output, "bar_sel": bar_output, "res_sel": res_output})





@general_pages_router.get("/restriction-output/all-possible-destinations-with-mask={mask_output}/bar={bar_output}/restaurant={res_output}/from-origin={origin_country}/for={username}")
async def homelist2(request:Request, mask_output:str, bar_output:str, res_output:str, origin_country:str, username:str):
    country_code = {
        'Afghanistan': 'AF', 'Albania': 'AL', 'Algeria': 'DZ', 'American-Samoa': 'AS', 'Angola': 'AO', 'Anguilla': 'AI', 'Antigua-and-Barbuda': 'AG', 'Argentina': 'AR', 'Armenia': 'AM', 
        'Aruba': 'AW', 'Australia': 'AU', 'Austria': 'AT', 'Azerbaijan': 'AZ', 'The-Bahamas': 'BS', 'Bahrain': 'BH', 'Bangladesh': 'BD', 'Barbados': 'BB', 'Belarus': 'BY', 'Belgium': 'BE', 
        'Belize': 'BZ', 'Benin': 'BJ', 'Bermuda': 'BM', 'Bhutan': 'BT', 'Bolivia': 'BO', 'Bosnia-and-Herzegovina': 'BA', 'Botswana': 'BW', 'Brazil': 'BR', 'Brunei-Darussalam': 'BN', 
        'Bulgaria': 'BG', 'Burkina-Faso': 'BF', 'Burundi': 'BI', 'Cape-Verde': 'CV', 'Cambodia': 'KH', 'Cameroon': 'CM', 'Canada': 'CA', 'Caribbean-Netherlands': 'BQ', 
        'Cayman-Islands': 'KY', 'Central-African-Republic': 'CF', 'Chad': 'TD', 'Chile': 'CL', 'China': 'CN', 'Colombia': 'CO', 'Comoros': 'KM', 'Democratic-Republic-of-the-Congo': 'CD', 
        'Republic-of-the-Congo': 'CG', 'Cook-Islands': 'CK', 'Costa-Rica': 'CR', 'Croatia': 'HR', 'Cuba': 'CU', 'Curacao': 'CW', 'Cyprus': 'CY', 'Czech-Republic': 'CZ', 'Ivory-Coast': 'CI', 
        'Denmark': 'DK', 'Djibouti': 'DJ', 'Dominica': 'DM', 'Dominican-Republic': 'DO', 'Ecuador': 'EC', 'Egypt': 'EG', 'El-Salvador': 'SV', 'Equatorial-Guinea': 'GQ', 'Eritrea': 'ER', 
        'Estonia': 'EE', 'Eswatini': 'SZ', 'Ethiopia': 'ET', 'Falkland-Islands-Islas-Malvinas': 'FK', 'Faroe-Islands': 'FO', 'Fiji': 'FJ', 'Finland': 'FI', 'France': 'FR', 
        'French-Guiana': 'GF', 'French-Polynesia': 'PF', 'Gabon': 'GA', 'Gambia': 'GM', 'Georgia': 'GE', 'Germany': 'DE', 'Ghana': 'GH', 'Gibraltar': 'GI', 'Greece': 'GR', 
        'Greenland': 'GL', 'Grenada': 'GD', 'Guadeloupe': 'GP', 'Guam': 'GU', 'Guatemala': 'GT', 'Guinea': 'GN', 'Guinea-Bissau': 'GW', 'Guyana': 'GY', 'Haiti': 'HT', 'Honduras': 'HN', 
        'Hong-Kong': 'HK', 'Hungary': 'HU', 'Iceland': 'IS', 'India': 'IN', 'Indonesia': 'ID', 'Iraq': 'IQ', 'Ireland': 'IE', 'Israel': 'IL', 'Italy': 'IT', 'Jamaica': 'JM', 'Japan': 'JP', 
        'Jersey': 'JE', 'Jordan': 'JO', 'Kazakhstan': 'KZ', 'Kenya': 'KE', 'Kiribati': 'KI', 'Kosovo': 'XK', 'North-Korea': 'KP', 'South-Korea': 'KR', 'Kuwait': 'KW', 'Kyrgyzstan': 'KG', 
        'Laos': 'LA', 'Latvia': 'LV', 'Lebanon': 'LB', 'Lesotho': 'LS', 'Liberia': 'LR', 'Libya': 'LY', 'Liechtenstein': 'LI', 'Lithuania': 'LT', 'Luxembourg': 'LU', 'Macau': 'MO', 
        'Madagascar': 'MG', 'Malawi': 'MW', 'Malaysia': 'MY', 'Maldives': 'MV', 'Mali': 'ML', 'Malta': 'MT', 'Marshall-Islands': 'MH', 'Martinique': 'MQ', 'Mauritania': 'MR', 
        'Mauritius': 'MU', 'Mayotte': 'YT', 'Mexico': 'MX', 'Federated-States-of-Micronesia': 'FM', 'Moldova': 'MD', 'Mongolia': 'MN', 'Montenegro': 'ME', 'Montserrat': 'MS', 'Morocco': 
        'MA', 'Mozambique': 'MZ', 'Myanmar': 'MM', 'Namibia': 'NA', 'Nauru': 'NR', 'Nepal': 'NP', 'Netherlands': 'NL', 'New-Caledonia': 'NC', 'New-Zealand': 'NZ', 'Nicaragua': 'NI', 
        'Niger': 'NE', 'Nigeria': 'NG', 'North-Macedonia': 'MK', 'Northern-Mariana-Islands': 'MP', 'Norway': 'NO', 'Oman': 'OM', 'Pakistan': 'PK', 'Palau': 'PW', 
        'Palestinian-Territories': 'PS', 'Panama': 'PA', 'Papua-New-Guinea': 'PG', 'Paraguay': 'PY', 'Peru': 'PE', 'Philippines': 'PH', 'Poland': 'PL', 'Portugal': 'PT', 
        'Puerto-Rico': 'PR', 'Qatar': 'QA', 'Romania': 'RO', 'Russia': 'RU', 'Rwanda': 'RW', 'Reunion': 'RE', 'Saint-Barthelemy': 'BL', 'Saint-Kitts-and-Nevis': 'KN', 'Saint-Lucia': 'LC', 
        'Saint-Martin': 'MF', 'Saint-Vincent-and-the-Grenadines': 'VC', 'Samoa': 'WS', 'Sao-Tome-and-Principe': 'ST', 'Saudi-Arabia': 'SA', 'Senegal': 'SN', 'Serbia': 'RS', 
        'Seychelles': 'SC', 'Sierra-Leone': 'SL', 'Singapore': 'SG', 'St-Maarten': 'SX', 'Slovakia': 'SK', 'Slovenia': 'SI', 'Solomon-Islands': 'SB', 'Somalia': 'SO', 'South-Africa': 'ZA', 
        'South-Sudan': 'SS', 'Spain': 'ES', 'Sri-Lanka': 'LK', 'Sudan': 'SD', 'Suriname': 'SR', 'Sweden': 'SE', 'Switzerland': 'CH', 'Syria': 'SY', 'Taiwan': 'TW', 'Tajikistan': 'TJ', 
        'Tanzania': 'TZ', 'Thailand': 'TH', 'East-Timor': 'TL', 'Togo': 'TG', 'Tonga': 'TO', 'Trinidad-and-Tobago': 'TT', 'Tunisia': 'TN', 'Turkey': 'TR', 'Turkmenistan': 'TM', 
        'Turks-and-Caicos-Islands': 'TC', 'Tuvalu': 'TV', 'Uganda': 'UG', 'Ukraine': 'UA', 'United-Arab-Emirates': 'AE', 'United-Kingdom': 'GB', 'United-States': 'US', 'Uruguay': 'UY', 
        'Uzbekistan': 'UZ', 'Vanuatu': 'VU', 'Venezuela': 'VE', 'Vietnam': 'VN', 'British-Virgin-Islands': 'VG', 'U-S-Virgin-Islands': 'VI', 'Wallis-and-Futuna': 'WF', 
        'Western-Sahara': 'EH', 'Yemen': 'YE', 'Zambia': 'ZM', 'Zimbabwe': 'ZW'}

    countries = ['Afghanistan', 'Albania', 'Algeria', 'American-Samoa', 'Angola', 'Anguilla', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'British-Virgin-Islands', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape-Verde', 'Caribbean-Netherlands', 'Cayman-Islands', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook-Islands', 'Costa-Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech-Republic', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'East-Timor', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland-Islands-Islas-Malvinas', 'Faroe-Islands', 'Federated-States-of-Micronesia', 'Fiji', 'Finland', 'France', 'French-Guiana', 'French-Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory-Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Caledonia', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North-Korea', 'North-Macedonia', 'Northern-Mariana-Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian-Territories', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto-Rico', 'Qatar', 'Republic-of-the-Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint-Barthelemy', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Martin', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Korea', 'South-Sudan', 'Spain', 'Sri-Lanka', 'St-Maarten', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'The-Bahamas', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks-and-Caicos-Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-States', 'Uruguay', 'U-S-Virgin-Islands', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis-and-Futuna', 'Western-Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
    länder = Empfehler(mask_output, bar_output, res_output, origin_country).oracle_picks()
    if länder == []:
        n_a = ["Sorry, but there are no results based on your selections"]
        saved = User_man(username).get_saved_trips()
        if saved == "no saved trips":
            saved_trips = ["No trip saved yet"]
            src = "404" 
            dest = "404" 
            link = "javascript:void(0);" 
            msg = "No trips found"
        else:
            saved_trips = saved
            src = saved_trips["origin"]
            dest = saved_trips["destination"]
            link = saved_trips["link"]
            msg = f"Travel from {src.title()} to {dest.title()}"
        return templates.TemplateResponse("general_pages/user_dashboard.html", {"request":request, "countries":countries, "länder": n_a, "origin_country": origin_country, "user": username,  "origin_sel": origin_country, "mask_sel": mask_output, "bar_sel": bar_output, "res_sel": res_output, "src": src, "dest": dest, "link": link, "msg": msg})
    else:

        flags = []
        brain = list(länder)
        for land in brain:
            broth = str(land)
            bent = broth.title()
            if bent in country_code:
                code_to_land = country_code.get(bent)
                flag_str = str(code_to_land)
                flag = flag_str.lower()
            flags.append(flag)

        src_ = []
        for item in flags:
            im = f"{item}.svg"
            src_.append(im)

        saved = User_man(username).get_saved_trips()
        if saved == "no saved trips":
            saved_trips = ["No trip saved yet"]
            src = "404" 
            dest = "404" 
            link = "javascript:void(0);" 
            msg = "No trips found"
        else:
            saved_trips = saved
            src = saved_trips["origin"]
            dest = saved_trips["destination"]
            link = saved_trips["link"]
            msg = f"Travel from {src.title()} to {dest.title()}"


        return templates.TemplateResponse("general_pages/user_dashboard.html", {"request":request, "user": username, "countries":countries, "länder": länder, "flags": flags, "source": src_, "origin_country": origin_country , "origin_sel": origin_country, "mask_sel": mask_output, "bar_sel": bar_output, "res_sel": res_output, "src": src, "dest": dest, "link": link, "msg": msg})