from eppy import modeleditor
from eppy.modeleditor import IDF

def VentingFactor(idf_file,VentingFactor):
	WindowOpeningObjects = idf_file.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]
	for i in range(0,len(WindowOpeningObjects)):
		WindowOpeningObjects[i].Width_Factor_for_Opening_Factor_2 = float(VentingFactor)**0.5
		WindowOpeningObjects[i].Height_Factor_for_Opening_Factor_2 = float(VentingFactor)**0.5

if __name__ == '__main':
	VentingFactor(idf_file,VentingFactor)