import sys
import csv

# make sure that we have enough command line argument
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

# open up data that we need of all the people and their genes
table = open(sys.argv[1], "r")

# read using a dictreader the csv and find the fields
reader = csv.DictReader(table)
fields = reader.fieldnames

# open the other file that will just be read as a long string of letters
file = open(sys.argv[2], "r")
person = file.read()

# set temporary variable equal to 0 and then also initalize a dictionary called officalcount
temp = 0

officialcount = {}

# This is where the bulk comes, start of with a for loop through all the fields
# Initalize the officialcount[STR] to 0 in case none of the string exists
# go through the entire length of a person doing the following check
# if the string from i to i plus the length of the STR actually equals the STR- add one to temp
# if that is the case then we want to check how long the string is so...
# we start at the point right after the first STR and then check the next length of the STR to see if it equals the TR
# if it does then add another to temp
# if there is no official count then set it equal to temp
# then after we have more than one temp, compare the new temp to the official count and take the max
# that will ensure that the longest string is taken into consideration
# set temp equal to 0

for STR in fields[1:]:
    officialcount[STR] = 0
    for i in range(len(person)):
        if person[i: i+len(STR)] == STR:
            temp += 1
            while True:
                if person[i+temp * len(STR): i + temp * len(STR) + len(STR)] == STR:
                    temp += 1
                else:
                    break

            if not officialcount.get(STR):
                officialcount[STR] = temp
            else:
                officialcount[STR] = max(temp, officialcount[STR])
            temp = 0

# go through the name in reader
# we will start off with person correct equalling tru
# looking at the STR's if the STR in relation to name is not equal to the string of the official count STR then
# then just place person correct to be false
# however if it is true then print the name and quit
# if the case is actually false then print no match

for name in reader:
    personcorrect = True
    for STR in fields[1:]:
        if not name[STR] == str(officialcount[STR]):
            personcorrect = False

    if personcorrect == True:
        print(name["name"])
        table.close()
        file.close()
        sys.exit()


table.close()
file.close()
print("No match")

