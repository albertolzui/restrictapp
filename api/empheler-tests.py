from empfehler import *

testrun = Empfehler("mandatory", "open","open", "Germany").oracle_picks()
#länder = []
#for dict in testrun:
#    land = dict.get("name")
#    länder.append(land)


print(testrun) 
#print(type(testrun[1]))