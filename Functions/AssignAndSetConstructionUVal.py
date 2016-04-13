from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Change the U-Value of the specified construction and assign it to all the surface of the specified type that have a 'Outside Boundary Condition' set to 'Outdoors'.
# Important Notes: 
#				- The specified construction should have an insulation material named after the construction. 
#				  For example, if the name of the construction is  'Construction 1' the name of the insulation material should be 'Construction 1 Insulation'.
#				- The insulation material has to be defined using the MATERIAL EnergyPlus object.
#				- The update to the U-Value of the construction is done by adjusting the thickness of the insulation material.
# Arg. Values: 
#				- Surface Type: Wall, Roof, Floor.
#				- Construction: Any construction available in the model that matches the above specification.
#				- U-Vaule: Any > 0.

def AssignAndSetConstructionUVal(idf_file,*args):
	# Define the Unit Registry used for unit conversion
	ureg = UnitRegistry()
		
	# Object and variables initialization
	SurfaceType = args[0][0]
	ConstructionName = args[0][1]
	UValue = args[0][2]	
	ConstructionObjects = idf_file.idfobjects["CONSTRUCTION"]
	MaterialObjects = idf_file.idfobjects["MATERIAL"]
	BuildingSurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	ConstructionRVal = 0
	
	# Calculate the R-Value of the specified construction w/o the insulation layer
	for i in range(0,len(ConstructionObjects)):
		if ConstructionObjects[i].Name == ConstructionName:
			for j in range(1,len(ConstructionObjects[i].fieldnames)):
				for k in range (0,len(MaterialObjects)):
					if MaterialObjects[k].Name == ConstructionObjects[i].fieldnames[j] and MaterialObjects[k].Name <> ConstructionName + " Insulation":
						ConstructionRVal = ConstructionRVal + (MaterialObjects[k].Thickness / MaterialObjects[k].Conductivity)
					elif MaterialObjects[k].Name == ConstructionName + " Insulation":
						CondIns = MaterialObjects[k].Conductivity
	
	# Conversion of the R-Value to IP units
	ConstructionRVal = ConstructionRVal*(ureg.meter**2)*ureg.degK/ureg.watt
	ConstructionRVal = ConstructionRVal.to(ureg.hour*(ureg.foot**2)*ureg.delta_degF/ureg.btu)
	ConstructionRVal = ConstructionRVal.magnitude
	
	# Adjust the calculated R-Value to take into account the air films (as defined by ASHRAE 90.1 Section A9.4.1)
	if SurfaceType == "Wall":
		ConstructionRVal = ConstructionRVal + 0.68 + 0.17
	elif SurfaceType == "Roof":
		ConstructionRVal = ConstructionRVal + 0.61 + 0.17
	elif SurfaceType == "Floor":
		ConstructionRVal = ConstructionRVal + 0.92 + 0.17	
		
	# Conversion of the R-Value to SI units
	ConstructionRVal = ConstructionRVal*ureg.hour*(ureg.foot**2)*ureg.delta_degF/ureg.btu
	ConstructionRVal = ConstructionRVal.to((ureg.meter**2)*ureg.degK/ureg.watt)
	ConstructionRVal = ConstructionRVal.magnitude
	
	# Conversion of the input U-Value to SI
	UValue = float(UValue)*ureg.btu/(ureg.hour*(ureg.foot**2)*ureg.delta_degF)
	UValue = UValue.to(ureg.watt/((ureg.meter**2)*ureg.degK))
	UValue = UValue.magnitude
	
	# Calculates the insulation layer R-Value
	RValIns = (1/UValue) - ConstructionRVal
	ThickIns = RValIns * CondIns
	
	# Adjust the insulation material's thickness to match the calculated R-Value
	for l in range (0,len(MaterialObjects)):
		if MaterialObjects[l].Name == ConstructionName + " Insulation":
			MaterialObjects[l].Thickness = ThickIns

	# Assign the updated construction to all the surface of the specified type
	for i in range(0,len(BuildingSurfaceObjects)):
		if BuildingSurfaceObjects[i].Surface_Type == SurfaceType and BuildingSurfaceObjects[i].Outside_Boundary_Condition == 'Outdoors':
			BuildingSurfaceObjects[i].Construction_Name = ConstructionName

if __name__ == '__main':
	AssignAndSetConstructionUVal(idf_file,SurfaceType,ConstructionName,UValue)