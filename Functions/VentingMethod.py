from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Set the venting method
# Arg. Values: ASHRAE55Adaptive, Temperature

def VentingMethod(idf_file,VentingMethod):
	AFNZoneObjects = idf_file.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
	for i in range(0,len(AFNZoneObjects)):
		AFNZoneObjects[i].Ventilation_Control_Mode = VentingMethod

if __name__ == '__main':
	VentingMethod(idf_file,VentingMethod)