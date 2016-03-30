from eppy import modeleditor
from eppy.modeleditor import IDF

def WindowSHGC(idf_file,WindowSHGC):
	WindowObjects = idf_file.idfobjects["WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM"]
	for i in range(0,len(WindowObjects)):
		WindowObjects[i].Solar_Heat_Gain_Coefficient = WindowSHGC

if __name__ == '__main':
	WindowSHGC(idf_file,WindowSHGC)