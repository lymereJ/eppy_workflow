from eppy import modeleditor
from eppy.modeleditor import IDF

def Roof(idf_file,Roof):
	if Roof == "Y":
		BuildingSurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
		for i in range(0,len(BuildingSurfaceObjects)):
			if BuildingSurfaceObjects[i].Name == "Top Surface":
				BuildingSurfaceObjects[i].Outside_Boundary_Condition = "Outdoors"
				BuildingSurfaceObjects[i].Construction_Name = "Roof Construction"

if __name__ == '__main':
	Roof(idf_file,Roof)