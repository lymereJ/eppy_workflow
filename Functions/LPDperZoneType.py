from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Creates a LIGHT object with specified LPD and assign it to the ZONELIST object that matches the zone type specified as input.
#			If the object already exist, it will just be modified.			
# Important Note: 
#				- A ZONELIST object must be created for each zone type.
#				- use the CreateAndAssignZoneTypes.py script to do that faster.
# Arg. Values: 
#				- LPD: Any > 0.
#				- ZoneType: Any available zone type name.
#				- ScheduleName: Any available schedule name.

def LPDperZoneType(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()
	
	# Object and variables initialization	
	LPD = args[0][0]
	ZoneType = args[0][1]
	ScheduleName = args[0][2]
	if len(args[0]) == 5:
		FracRad = args[0][3]
		FracVis	= args[0][4]
	LightsObjects = idf_file.idfobjects["LIGHTS"]
	LightsObjectIdx = 0
	
	# Conversion to Float and from IP to SI
	LPD = float(LPD)
	LPDinIP = LPD*ureg.watt/ureg.foot**2
	LPDinSI = LPDinIP.to((ureg.watt)/ureg.meter**2)	
	
	# Check if an object for this space type already exist
	if len(LightsObjects) > 0:
		for i in range(0,len(LightsObjects)):
			if LightsObjects[i].Name == ZoneType + " LPD":
				
				# Set the index of the LIGHTS objects
				LightsObjectIdx = i
				
				# Assign the new LPD, Zone Type and Lighting Fraction
				LightsObjects[i].Watts_per_Zone_Floor_Area = LPDinSI.magnitude
				LightsObjects[i].Zone_or_ZoneList_Name = ZoneType
				if len(args[0]) == 5:
					LightsObjects[i].Fraction_Radiant = FracRad
					LightsObjects[i].Fraction_Visible = FracVis
				else:
					LightsObjects[i].Fraction_Radiant = 0.72
					LightsObjects[i].Fraction_Visible = 0.18	
					
	if LightsObjectIdx == 0:
		
		# Create and defines the LIGHT object
		NewLightsObject = idf_file.newidfobject("LIGHTS")
		NewLightsObject.Name = ZoneType + " LPD"
		NewLightsObject.Zone_or_ZoneList_Name = ZoneType
		NewLightsObject.Schedule_Name = ScheduleName
		NewLightsObject.Design_Level_Calculation_Method = "Watts/Area"
		NewLightsObject.Watts_per_Zone_Floor_Area = LPDinSI
		
		# If FracRad and FracVis are not provided, assumed to be Surface Mount. Values as per the EnergyPlus I/O reference manual
		if len(args[0]) == 5:
			NewLightsObject.Fraction_Radiant = FracRad
			NewLightsObject.Fraction_Visible = FracVis
		else:
			NewLightsObject.Fraction_Radiant = 0.72
			NewLightsObject.Fraction_Visible = 0.18
		
if __name__ == '__main':
	LPDperZoneType(idf_file,*args)