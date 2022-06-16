from empfehler import *

testrun = Empfehler("mandatory", "open","open", "Germany").oracle_picks()
länder = []
for dict in testrun:
    land = dict.get("name")
    länder.append(land)


print(länder) 
#print(type(testrun[1]))