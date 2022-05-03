from crawler import Web_Crawler

bass = Web_Crawler("NIGERIA", "DE").clean_up_sections()

for i in range(len(bass)):
    print (i, end = " ")
    print (bass[i],"\n")
    




