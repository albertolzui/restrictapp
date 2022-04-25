import re
from numpy import append
import requests
from bs4 import BeautifulSoup 
#from selenium import cssselector

destination = input("destination? ")
origin = input("origin ?")

ori= "origin="+origin
url = 'https://www.kayak.com/travel-restrictions/'+ destination + '?' + ori
exception_US_to_austria = "https://www.kayak.com/travel-restrictions/austria?origin=US"


r = requests.get(url)

src = r.content

soup = BeautifulSoup(src, 'html.parser')

links = soup.find_all("a")

divs = soup.find_all("div")

h5s = soup.find_all("h5")

h5str = str(h5s)

divsy = str(divs)

paragraphs = soup.find_all("p")

paragraph_to_str = str(paragraphs)



p_tag = BeautifulSoup(paragraph_to_str, "html.parser")

div_tag = BeautifulSoup(divsy, "html.parser")

h5_tag = BeautifulSoup(h5str, "html.parser")


alt_paragraph_extractor = soup.select("div > p")
alt_paragraph_extractor_to_string = str(alt_paragraph_extractor)
parsed_paragraphs = BeautifulSoup(alt_paragraph_extractor_to_string, "html.parser")




result_quar_req = parsed_paragraphs.find_all('p')
quar_req1_str = str(result_quar_req[4])
quar_req1_grab = re.search('>(.*)<', quar_req1_str)
quar_req1 = []
quar_r1 = quar_req1_grab.group(1)
quar_req1.append(quar_r1)

quar_req2_str = str(result_quar_req[5])
quar_req2_grab = re.search('>(.*)<', quar_req2_str)
quar_req2 = []
quar_r2 = quar_req2_grab.group(1)
quar_req2.append(quar_r2)

quar_r = quar_r1 + quar_r2
#print(quar_r)

#res = parsed_paragraphs.get_text()
resd = soup.get_text(" | ")

#print(resd)

mugl = list(resd.split("|"))
del mugl[:17]




for i in range(len(mugl)):
    print (i, end = " ")
    print (mugl[i])

#headings = ["Travel Restrictions", "entry details and exceptions", "Traveling from" ]

def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list

#kugl = get_index_positions(mugl, " Traveling from Germany to Nigeria")
#print(kugl)




#print(mugl)