from eppy import modeleditor
from eppy.modeleditor import IDF

def Length(idf_file,Length):
	BuildingSurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	Length = float(Length) * 0.3048
	for i in range(0,len(BuildingSurfaceObjects)):
		if BuildingSurfaceObjects[i].Vertex_1_Ycoordinate == 15.24:
			BuildingSurfaceObjects[i].Vertex_1_Ycoordinate = Length
		elif BuildingSurfaceObjects[i].Vertex_1_Ycoordinate == -15.24:
			BuildingSurfaceObjects[i].Vertex_1_Ycoordinate = -1 * Length

		if BuildingSurfaceObjects[i].Vertex_2_Ycoordinate == 15.24:
			BuildingSurfaceObjects[i].Vertex_2_Ycoordinate = Length
		elif BuildingSurfaceObjects[i].Vertex_2_Ycoordinate == -15.24:
			BuildingSurfaceObjects[i].Vertex_2_Ycoordinate = -1 * Length	

		if BuildingSurfaceObjects[i].Vertex_3_Ycoordinate == 15.24:
			BuildingSurfaceObjects[i].Vertex_3_Ycoordinate = Length
		elif BuildingSurfaceObjects[i].Vertex_3_Ycoordinate == -15.24:
			BuildingSurfaceObjects[i].Vertex_3_Ycoordinate = -1 * Length

		if BuildingSurfaceObjects[i].Vertex_4_Ycoordinate == 15.24:
			BuildingSurfaceObjects[i].Vertex_4_Ycoordinate = Length
		elif BuildingSurfaceObjects[i].Vertex_4_Ycoordinate == -15.24:
			BuildingSurfaceObjects[i].Vertex_4_Ycoordinate = -1 * Length		

	WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
	Length = (Length / 0.3048 - 0.1) * 0.3048
	for i in range(0,len(WindowObjects)):
		if WindowObjects[i].Vertex_1_Ycoordinate == 15.20952:
			WindowObjects[i].Vertex_1_Ycoordinate = Length
		elif WindowObjects[i].Vertex_1_Ycoordinate == -15.20952:
			WindowObjects[i].Vertex_1_Ycoordinate = -1 * Length

		if WindowObjects[i].Vertex_2_Ycoordinate == 15.20952:
			WindowObjects[i].Vertex_2_Ycoordinate = Length
		elif WindowObjects[i].Vertex_2_Ycoordinate == -15.20952:
			WindowObjects[i].Vertex_2_Ycoordinate = -1 * Length	

		if WindowObjects[i].Vertex_3_Ycoordinate == 15.20952:
			WindowObjects[i].Vertex_3_Ycoordinate = Length
		elif WindowObjects[i].Vertex_3_Ycoordinate == -15.20952:
			WindowObjects[i].Vertex_3_Ycoordinate = -1 * Length

		if WindowObjects[i].Vertex_4_Ycoordinate == 15.20952:
			WindowObjects[i].Vertex_4_Ycoordinate = Length
		elif WindowObjects[i].Vertex_4_Ycoordinate == -15.20952:
			WindowObjects[i].Vertex_4_Ycoordinate = -1 * Length				

if __name__ == '__main':
	Length(idf_file,Length)