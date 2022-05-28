#from crawler_for_api import *
from crawler_for_api_revised import *


#state = Web_Crawler("thailand", "DE").link_lister()
#del state[0:24]
#boil = " ".join()
"""
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
"""

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
clay = Web_Crawler("nigeria", "DE").crawl_into_db() 
print(clay)