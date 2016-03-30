from eppy import modeleditor
from eppy.modeleditor import IDF

def Orientation(idf_file,DegFromNorth):
	BuildingObjects = idf_file.idfobjects["BUILDING"]
	for i in range(0,len(BuildingObjects)):
		BuildingObjects[i].North_Axis = DegFromNorth

if __name__ == '__main':
	Orientation(idf_file,DegFromNorth)