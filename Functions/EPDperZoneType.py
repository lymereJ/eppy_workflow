from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Creates a ElectricEquipment object with specified EPD and assign it to the ZONELIST object that matches the zone type specified as input.
#			If the object already exist, it will just be modified.			
# Important Notes: 
#				- A ZONELIST object must be created for each zone type.
#				- use the CreateAndAssignZoneTypes.py script to do that faster.
# Arg. Values: 
#				- EPD: Any > 0.
#				- ZoneType: Any available zone type name.
#				- ScheduleName: Any available schedule name.

def EPDperZoneType(idf_file,*args):
	# Define the Unit Registry used for unit conversion
	ureg = UnitRegistry()
	
	# Object and variables initialization	
	LPD = args[0][0]
	ZoneType = args[0][1]
	ScheduleName = args[0][2]
	if len(args[0]) == 4:
		FracRad = args[0][3]
	ElectricEquipmentObjects = idf_file.idfobjects["ELECTRICEQUIPMENT"]
	ElectricEquipmentObjectIdx = 0
	
	# Conversion to Float and from IP to SI
	EPD = float(LPD)
	EPDinIP = EPD*ureg.watt/ureg.foot**2
	EPDinSI = EPDinIP.to((ureg.watt)/ureg.meter**2)	
	
	# Check if an object for this space type already exist
	if len(ElectricEquipmentObjects) > 0:
		for i in range(0,len(ElectricEquipmentObjects)):
			if ElectricEquipmentObjects[i].Name == ZoneType + " EPD":
				
				# Set the index of the ELECTRICEQUIPMENT objects
				ElectricEquipmentObjectIdx = i
				
				# Assign the new LPD, Zone Type and Lighting Fraction
				ElectricEquipmentObjects[i].Watts_per_Zone_Floor_Area = EPDinSI.magnitude
				ElectricEquipmentObjects[i].Zone_or_ZoneList_Name = ZoneType
				if len(args[0]) == 4:
					ElectricEquipmentObjects[i].Fraction_Radiant = FracRad
				else:
					ElectricEquipmentObjects[i].Fraction_Radiant = 0.7
					
	if ElectricEquipmentObjectIdx == 0:
		
		# Create and defines the ELECTRICEQUIPMENT object
		NewElectricEquipmentObject = idf_file.newidfobject("ELECTRICEQUIPMENT")
		NewElectricEquipmentObject.Name = ZoneType + " EPD"
		NewElectricEquipmentObject.Zone_or_ZoneList_Name = ZoneType
		NewElectricEquipmentObject.Schedule_Name = ScheduleName
		NewElectricEquipmentObject.Design_Level_Calculation_Method = "Watts/Area"
		NewElectricEquipmentObject.Watts_per_Zone_Floor_Area = EPDinSI.magnitude
		
		# If FracRad and FracVis are not provided, assumed to be Surface Mount. Values as per the EnergyPlus I/O reference manual
		if len(args[0]) == 4:
			NewElectricEquipmentObject.Fraction_Radiant = FracRad
		else:
			NewElectricEquipmentObject.Fraction_Radiant = 0.7
		
if __name__ == '__main':
	EPDperZoneType(idf_file,*args)