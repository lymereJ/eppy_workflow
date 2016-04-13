from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create and Assign a window Construction to the windows facing the specified orientation and adjust the U-Factor and and SHGC of the WindowMaterial:SimpleGlazingSystem
# Important Notes:
#				- 
# Arg. Values: 
#				- Ufactor: Any > 0.
#				- SHGC: Any > 0.
#				- Orientation: North, East, South, Weast, and Any.

def TranslatedOrientation(Azimuth):
	if Azimuth >= 360:
		Azimuth = Azimuth - 360
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

def CreateAndAssignAndSetWindThermProp(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()
	
	# Object and variables initialization
	Ufactor = args[0][0]
	SHGC = args[0][1]
	VT = args[0][2]
	Orientation = args[0][3]
	WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
	BuildingObjects = idf_file.idfobjects["BUILDING"]
	NorthAxis = BuildingObjects[0].North_Axis	
	
	# Conversion of the UFactor specified in IP to SI units
	Ufactor = float(Ufactor)
	UfactorIP = Ufactor*ureg.btu/(ureg.hour*(ureg.foot**2)*ureg.delta_degF)
	UfactorSI = UfactorIP.to((ureg.watt/ureg.meter**2/ureg.degK))
	
	# Create the new WindowMaterial:SimpleGlazingSystem
	NewWinWindowMaterialSimpleGlazingSystem = idf_file.newidfobject("WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM")
	NewWinWindowMaterialSimpleGlazingSystem.Name = "WindowLayer-" + str(Ufactor) + "-" + str(SHGC) + "-" + Orientation
	NewWinWindowMaterialSimpleGlazingSystem.UFactor = UfactorSI.magnitude	
	NewWinWindowMaterialSimpleGlazingSystem.Solar_Heat_Gain_Coefficient = SHGC
	NewWinWindowMaterialSimpleGlazingSystem.Visible_Transmittance = VT
	
	# Create the new Construction
	NewWindowConstruction = idf_file.newidfobject("CONSTRUCTION")
	NewWindowConstruction.Name = "Window-" + str(Ufactor) + "-" + str(SHGC) + "-" + Orientation
	NewWindowConstruction.Outside_Layer = "WindowLayer-" + str(Ufactor) + "-" + str(SHGC) + "-" + Orientation

	# Assign the new Construction to the windows facing the specified orientation
	for i in range(0,len(WindowObjects)):
		if WindowObjects[i].Surface_Type == "Window" and (TranslatedOrientation(WindowObjects[i].azimuth + NorthAxis) == Orientation or Orientation == "Any"):
			WindowObjects[i].Construction_Name = "Window-" + str(Ufactor) + "-" + str(SHGC) + "-" + Orientation

if __name__ == '__main':
	CreateAndAssignAndSetWindThermProp(idf_file,*args)