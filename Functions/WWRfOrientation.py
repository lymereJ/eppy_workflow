from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Set the WWR by adjusting the height of the windows.
# Important Note: 
#				- The windows needs to be rectangles.
# Arg. Values: Any > 0.

def TranslatedOrientation(Azimuth):
	if Azimuth <= 45:
		return "North"
	elif Azimuth <= 135:
		return "East"
	elif Azimuth <= 225:
		return "South"
	elif Azimuth <= 315:
		return "West"
	else:
		return "North"

def WWRfOrientation(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	WWR = args[0][0]
	Orientation = args[0][1]
	TotalWindowArea = 0
	TotalOpaqueArea = 0
	WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
	OpaqueObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	
	# Retrieve the total net window area
	for i in range(0,len(WindowObjects)):
		if WindowObjects[i].Surface_Type == "Window" and (TranslatedOrientation(WindowObjects[i].azimuth) == Orientation or Orientation == "Any"):
			TotalWindowArea = TotalWindowArea + WindowObjects[i].area
	
	# Retrieve the total gross wall area
	for i in range (0,len(OpaqueObjects)):
		if OpaqueObjects[i].Outside_Boundary_Condition == "Outdoors" and OpaqueObjects[i].Surface_Type == "Wall" and (TranslatedOrientation(OpaqueObjects[i].azimuth) == Orientation or Orientation == "Any"):
			TotalOpaqueArea = TotalOpaqueArea + OpaqueObjects[i].area
	
	# Determine the reference WWR and the height modifier based on the user input WWR
	WWR_ref = TotalWindowArea / TotalOpaqueArea
	HeightModifier = WWR_ref / float(WWR)
	
	# Adjust the height of the windows according to the modifier previously calculated
	for i in range(0, len(WindowObjects)):
		if TranslatedOrientation(WindowObjects[i].azimuth) == Orientation or Orientation == "Any":
			MaxHgt = max(WindowObjects[i].Vertex_1_Zcoordinate,WindowObjects[i].Vertex_2_Zcoordinate,WindowObjects[i].Vertex_3_Zcoordinate,WindowObjects[i].Vertex_4_Zcoordinate)
			MinHgt = min(WindowObjects[i].Vertex_1_Zcoordinate,WindowObjects[i].Vertex_2_Zcoordinate,WindowObjects[i].Vertex_3_Zcoordinate,WindowObjects[i].Vertex_4_Zcoordinate)
			WindowHeight = MaxHgt - MinHgt
			if WindowObjects[i].Vertex_1_Zcoordinate == MaxHgt:
				WindowObjects[i].Vertex_1_Zcoordinate =  WindowHeight / HeightModifier + MinHgt
			if WindowObjects[i].Vertex_2_Zcoordinate == MaxHgt:
				WindowObjects[i].Vertex_2_Zcoordinate =  WindowHeight / HeightModifier + MinHgt
			if WindowObjects[i].Vertex_3_Zcoordinate == MaxHgt:
				WindowObjects[i].Vertex_3_Zcoordinate =  WindowHeight / HeightModifier + MinHgt			
			if WindowObjects[i].Vertex_4_Zcoordinate == MaxHgt:
				WindowObjects[i].Vertex_4_Zcoordinate =  WindowHeight / HeightModifier + MinHgt			
			
if __name__ == '__main':
	WWRfOrientation(idf_file,WWR,Orientation)