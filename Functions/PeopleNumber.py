from eppy import modeleditor
from eppy.modeleditor import IDF

def PeopleNumber(idf_file,PeopleNumber):
	PeopleObjects = idf_file.idfobjects["PEOPLE"]
	for i in range(0,len(PeopleObjects)):
		PeopleObjects[i].Number_of_People = PeopleNumber

if __name__ == '__main':
	PeopleNumber(idf_file,PeopleNumber)