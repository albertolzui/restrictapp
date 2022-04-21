import re
from numpy import append
import requests
from bs4 import BeautifulSoup 

result = requests.get

destination = input("destination? ")
origin = input("origin ?")
ori= "origin="+origin
url = 'https://www.kayak.com/travel-restrictions/'+ destination + '?' + ori
exception_US_to_austria = "https://www.kayak.com/travel-restrictions/austria?origin=US"


r = requests.get(url)

src = r.content

soup = BeautifulSoup(src, 'lxml')

links = soup.find_all("a")

divs = soup.find_all("div")

divsy = str(divs)

paragraphs = soup.find_all("p")

paragraph_to_str = str(paragraphs)

p_tag = BeautifulSoup(paragraph_to_str, "lxml")

div_tag = BeautifulSoup(divsy, "lxml")

# Get page title
result_title_fetch = div_tag.find_all('h1')[1]
title = [] 
for child in result_title_fetch.children:
    title.append(child)
print("Page Title: ", *title)

# Get Border Status
result_bs_fetch = div_tag.find_all('span')[20]
border_status = [] 
for child in result_bs_fetch.children:
    border_status.append(child)
print("Border Status: ", *border_status)

# Get Vaccination Rate
result_vr_fetch = div_tag.find_all('span')[21]
vac_rate = [] 
for child in result_vr_fetch.children:
    vac_rate.append(child)
print("Vaccination Rate: ", *vac_rate)

# Get Summary of Vaccination Requirements
result_vrs_fetch = div_tag.find_all('span')[23]
vrs_to_str = str(result_vrs_fetch)
vrs_rmv_b_tag_opening = vrs_to_str.replace('<b>', '')
vrs_rmv_b_tag_closing = vrs_rmv_b_tag_opening.replace('</b>', '')
vrs_grab = re.search('>(.*)<', vrs_rmv_b_tag_closing)
vac_req_summary1 = vrs_grab.group(1)

result_vrs_fetch2 = div_tag.find_all('span')[25]
vrs_to_str2 = str(result_vrs_fetch2)
vrs_rmv_b_tag_opening2 = vrs_to_str2.replace('<b>', '')
vrs_rmv_b_tag_closing2 = vrs_rmv_b_tag_opening2.replace('</b>', '')
vrs_grab2 = re.search('>(.*)<', vrs_rmv_b_tag_closing2)
vac_req_summary2 = vrs_grab2.group(1)

vac_req_summary = vac_req_summary1 + ' ' + vac_req_summary2
print("Vaccination Requirement Summary: ", vac_req_summary)

#vac_req_summary = [] 
#for child in result_vrs_fetch.children:
#    vac_req_summary.append(child)

#result_vrs_fetch2 = div_tag.find_all('span')[25]
#for child in result_vrs_fetch2.children:
#    vac_req_summary.append(child)
#print("Vaccination Requirement Summary: ", *vac_req_summary, end=" ", sep="")

# Get Note to Vaccination Requirement Summary
result_note_to_vrs_fetch = p_tag.find_all('p')[1]
note_to_vac_req_summary = [] 
for child in result_note_to_vrs_fetch.children:
    note_to_vac_req_summary.append(child)
print("Note to Vaccination Requirement Summary: ", *note_to_vac_req_summary)


# Get Subheading Title: Entry Details and Exceptions: sh_ede)
result_sh_ede_fetch = div_tag.find_all('h2')[0]
sh_ede = [] 
for child in result_sh_ede_fetch.children:
    sh_ede.append(child)
print("Sub Heading Title: ", *sh_ede)


# Get Note from Entry Details and Exceptions
result_note_from_ede = p_tag.find_all('p')[2]
note_from_ede = [] 
for child in result_note_from_ede.children:
    note_from_ede.append(child)
print("Note from Entry Details and Exceptions: ", *note_from_ede)


# Get Subheading Title: COVID-19 Testing Requirements : sh_ctr
result_sh_ctr_fetch = div_tag.find_all('h5')[0]
sh_ctr_to_str = str(result_sh_ctr_fetch)
sh_ctr_grab = re.search('n>(.*)<', sh_ctr_to_str)
sh_ctr = sh_ctr_grab.group(1)
print("Sub Heading Title: ", *sh_ctr)


# Get COVID-19 Testing Requirements - Test Type: sh_test_type (subheading)
result_sh_test_type_fetch = div_tag.find_all('h6')[0]
sh_test_type = [] 
for child in result_sh_test_type_fetch.children:
    sh_test_type.append(child)
print("Sub Heading Title: ", *sh_test_type)


# Get Note from Test Type: test_type
result_note_from_test_type = p_tag.find_all('p')[3]
note_from_test_type = [] 
for child in result_note_from_test_type.children:
    note_from_test_type.append(child)
if url == exception_US_to_austria:
    result_note_from_test_type2 = p_tag.find_all('p')[4]
    for child in result_note_from_test_type2.children:
        note_from_test_type.append(child)

print("Note from Test Type: ", *note_from_test_type)


# Get COVID-19 Testing Requirements - Test Type Details and Exceptions : sh_test_type_d_and_e (subheading)
result_sh_test_type_d_and_e_fetch = div_tag.find_all('h6')[1]
sh_test_type_d_and_e = [] 
for child in result_sh_test_type_d_and_e_fetch.children:
    sh_test_type_d_and_e.append(child)
print("Sub Heading Title: ", *sh_test_type_d_and_e)


# Get Notes from Details and exceptions: note_from_d_and_e
result_note_from_d_and_e1 = div_tag.find_all('div')[34]
note_from_d_and_e = [] 
if url == exception_US_to_austria:
    for child in result_note_from_d_and_e1.children: 
        note_from_d_and_e.append(child)
else:
    for child in result_note_from_d_and_e1.children: 
        note_from_d_and_e.append(child)
    result_note_from_d_and_e2 = div_tag.find_all('div')[35]
    for child in result_note_from_d_and_e2.children:
        note_from_d_and_e.append(child)
print("Note from Test Type Details and Exceptions: ", *note_from_d_and_e, end=" ")


