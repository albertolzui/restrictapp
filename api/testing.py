from crawler_for_api import *

state = Web_Crawler("thailand", "DE").link_lister()

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



#print(Web_Crawler("czech-republic", "DE").cull_from_db())
#print(Web_Crawler("south-africa", "DE").country_name)
#if "Belaru Travel Restrictions" in co:
#    print("True")
#else:
print(state[1])