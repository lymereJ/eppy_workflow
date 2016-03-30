from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Change the SHGC value for the glazing
# Arg. Values: Any

def WindowSHGC(idf_file,WindowSHGC):
	WindowObjects = idf_file.idfobjects["WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM"]
	for i in range(0,len(WindowObjects)):
		WindowObjects[i].Solar_Heat_Gain_Coefficient = WindowSHGC

if __name__ == '__main':
	WindowSHGC(idf_file,WindowSHGC)