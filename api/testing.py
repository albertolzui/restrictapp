from crawler_for_api import *

#result1 = Web_Crawler("ghana", "DE").crawl_into_db() 
#result = Web_Crawler("ghana", "DE").update_db_entry()
#r = Web_Crawler("ghana", "DE").cull_from_db()
#b = r["date"]
#d = datetime.timedelta(days = 2)
#c = datetime.datetime.utcnow()
#f = c-b

#if f > d:
#    print("True")
#else:
#    print("False")
#print(type(f))
#print(c-b)
#print(c)
def do(destination, origin):
    check = Web_Crawler(destination, origin).cull_from_db()
    output = []
    if check:
        entry_date = check["date"]
        max_age_of_info = datetime.timedelta(days = 2)
        time_now = datetime.datetime.utcnow()
        duration_of_info = time_now - entry_date
        if duration_of_info < max_age_of_info:
            output.append(check)
            return output
    else:
        Web_Crawler(destination, origin).crawl_into_db()
        check = Web_Crawler(destination, origin).cull_from_db()
        if check:
            entry_date = check["date"]
            max_age_of_info = datetime.timedelta(days = 2)
            time_now = datetime.datetime.utcnow()
            duration_of_info = time_now - entry_date
            if duration_of_info < max_age_of_info:
                output.append(check)
                return output
                


print(do("france", "DE"))