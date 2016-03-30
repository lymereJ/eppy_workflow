from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

def WWR(idf_file,WWR):

	ureg = UnitRegistry()

	TotalWindowArea = 0
	TotalOpaqueArea = 0
	
	WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
	OpaqueObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	
	for i in range(0,len(WindowObjects)):
		if WindowObjects[i].Surface_Type == "Window":
			TotalWindowArea = TotalWindowArea + WindowObjects[i].area
	
	for i in range (0,len(OpaqueObjects)):
		if OpaqueObjects[i].Outside_Boundary_Condition == "Outdoors" and OpaqueObjects[i].Surface_Type == "Wall":
			TotalOpaqueArea = TotalOpaqueArea + OpaqueObjects[i].area
	
	WWR_ref = TotalWindowArea / TotalOpaqueArea
		
	HeightModifier = WWR_ref / float(WWR)
	
	for i in range(0, len(WindowObjects)):
		WindowHeight = WindowObjects[i].Vertex_1_Zcoordinate - WindowObjects[i].Vertex_2_Zcoordinate
		WindowObjects[i].Vertex_1_Zcoordinate =  WindowHeight / HeightModifier 
		WindowObjects[i].Vertex_4_Zcoordinate =  WindowHeight / HeightModifier 
	
if __name__ == '__main':
	WWR(idf_file,WWR)