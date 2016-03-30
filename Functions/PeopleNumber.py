from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Change the number of people
# Arg. Values: Any

def PeopleNumber(idf_file,PeopleNumber):
	PeopleObjects = idf_file.idfobjects["PEOPLE"]
	for i in range(0,len(PeopleObjects)):
		PeopleObjects[i].Number_of_People = PeopleNumber

if __name__ == '__main':
	PeopleNumber(idf_file,PeopleNumber)