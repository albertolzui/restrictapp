from crawler_for_api import *

state = Web_Crawler("czech-republic", "DE").clean_up_sections()
bait = state[5]



#print(Web_Crawler("czech-republic", "DE").cull_from_db())
#print(Web_Crawler("south-africa", "DE").country_name)
#if "Belaru Travel Restrictions" in co:
#    print("True")
#else:
print(bait)