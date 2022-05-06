from crawler import *

#cleaned_list_for_db = Web_Crawler("NIGERIA", "DE").clean_up_sections()
#write_into_db = Web_Crawler("NIGERIA", "DE").crawl_into_db()

#for i in range(len(cleaned_list_for_db)):
#    print (i, end = " ")
#    print (cleaned_list_for_db[i],"\n")
    



result = db.country_restrictions.find_one({"name": "NIGERIA"})
print(result)