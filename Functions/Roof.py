from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Change the unit from being a 'middle' unit to a 'top' (with a roof)
# Arg. Values: Y, N

def Roof(idf_file,Roof):
	if Roof == "Y":
		BuildingSurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
		for i in range(0,len(BuildingSurfaceObjects)):
			if BuildingSurfaceObjects[i].Name == "Top Surface":
				BuildingSurfaceObjects[i].Outside_Boundary_Condition = "Outdoors"
				BuildingSurfaceObjects[i].Construction_Name = "Roof Construction"

if __name__ == '__main':
	Roof(idf_file,Roof)