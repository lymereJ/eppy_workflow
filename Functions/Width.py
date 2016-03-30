from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Change the width of the test cell
# Arg. Values: Any

def Width(idf_file,Width):
	BuildingSurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	Width = float(Width) * 0.3048
	for i in range(0,len(BuildingSurfaceObjects)):
		if BuildingSurfaceObjects[i].Vertex_1_Xcoordinate == 6.096:
			BuildingSurfaceObjects[i].Vertex_1_Xcoordinate = Width
		elif BuildingSurfaceObjects[i].Vertex_1_Xcoordinate == -6.096:
			BuildingSurfaceObjects[i].Vertex_1_Xcoordinate = -1 * Width

		if BuildingSurfaceObjects[i].Vertex_2_Xcoordinate == 6.096:
			BuildingSurfaceObjects[i].Vertex_2_Xcoordinate = Width
		elif BuildingSurfaceObjects[i].Vertex_2_Xcoordinate == -6.096:
			BuildingSurfaceObjects[i].Vertex_2_Xcoordinate = -1 * Width	

		if BuildingSurfaceObjects[i].Vertex_3_Xcoordinate == 6.096:
			BuildingSurfaceObjects[i].Vertex_3_Xcoordinate = Width
		elif BuildingSurfaceObjects[i].Vertex_3_Xcoordinate == -6.096:
			BuildingSurfaceObjects[i].Vertex_3_Xcoordinate = -1 * Width

		if BuildingSurfaceObjects[i].Vertex_4_Xcoordinate == 6.096:
			BuildingSurfaceObjects[i].Vertex_4_Xcoordinate = Width
		elif BuildingSurfaceObjects[i].Vertex_4_Xcoordinate == -6.096:
			BuildingSurfaceObjects[i].Vertex_4_Xcoordinate = -1 * Width			
	
	WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
	Width = (Width / 0.3048 - 0.1) * 0.3048
	for i in range(0,len(WindowObjects)):
		if WindowObjects[i].Vertex_1_Xcoordinate == 6.06552:
			WindowObjects[i].Vertex_1_Xcoordinate = Width
		elif WindowObjects[i].Vertex_1_Xcoordinate == -6.06552:
			WindowObjects[i].Vertex_1_Xcoordinate = -1 * Width
			
		if WindowObjects[i].Vertex_2_Xcoordinate == 6.06552:
			WindowObjects[i].Vertex_2_Xcoordinate = Width
		elif WindowObjects[i].Vertex_2_Xcoordinate == -6.06552:
			WindowObjects[i].Vertex_2_Xcoordinate = -1 * Width	
			
		if WindowObjects[i].Vertex_3_Xcoordinate == 6.06552:
			WindowObjects[i].Vertex_3_Xcoordinate = Width
		elif WindowObjects[i].Vertex_3_Xcoordinate == -6.06552:
			WindowObjects[i].Vertex_3_Xcoordinate = -1 * Width
			
		if WindowObjects[i].Vertex_4_Xcoordinate == 6.06552:
			WindowObjects[i].Vertex_4_Xcoordinate = Width
		elif WindowObjects[i].Vertex_4_Xcoordinate == -6.06552:
			WindowObjects[i].Vertex_4_Xcoordinate = -1 * Width	

	AFNZoneObjects = idf_file.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
	for i in range(0,len(AFNZoneObjects)):
		AFNZoneObjects[i].Facade_Width = Width
	
if __name__ == '__main':
	Width(idf_file,Width)