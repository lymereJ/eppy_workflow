from eppy import modeleditor
from eppy.modeleditor import IDF

def VentingMethod(idf_file,VentingMethod):
	AFNZoneObjects = idf_file.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
	for i in range(0,len(AFNZoneObjects)):
		AFNZoneObjects[i].Ventilation_Control_Mode = VentingMethod

if __name__ == '__main':
	VentingMethod(idf_file,VentingMethod)