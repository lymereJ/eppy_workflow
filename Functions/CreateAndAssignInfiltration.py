from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create and Assign a ZoneInfiltration:DesignFlowRate and set it to the ZoneList specified
# Important Notes:
#				- Zone Types (via ZoneList objects) must be defined before calling this function
# Arg. Values: 
#				- ZoneType: Any Zone Type available in the model.
#				- ScheduleName: Any available schedule.
#				- Method: ACH or CFMperExtWallArea
#				- InfFlow : Any > 0.

def CreateAndAssignInfiltration(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()
	
	# Object and variables initialization
	ZoneType = args[0][0]
	ScheduleName = args[0][1]
	Method = args[0][2]
	InfFlow = args[0][3]
	
	# Create the new ZoneInfiltration:DesignFlowRate object based on the specified input and assign it to the specified ZoneType
	NewInfObject = idf_file.newidfobject("ZONEINFILTRATION:DESIGNFLOWRATE")
	NewInfObject.Name = "Infiltration " + ZoneType
	NewInfObject.Zone_or_ZoneList_Name = ZoneType
	NewInfObject.Schedule_Name = ScheduleName
	
	if Method == "ACH":
		NewInfObject.Design_Flow_Rate_Calculation_Method = "AirChanges/Hour"
		NewInfObject.Air_Changes_per_Hour = InfFlow
	elif Method == "CFMperExtWallArea":
		NewInfObject.Design_Flow_Rate_Calculation_Method = "Flow/ExteriorWallArea"
		InfFlow = float(InfFlow)
		InfFlowIP = InfFlow*(ureg.foot**3/ureg.minute)/ureg.foot**2
		InfFlowSI = InfFlowIP.to((ureg.meter**3/ureg.second)/ureg.meter**2)
		NewInfObject.Flow_per_Exterior_Surface_Area = InfFlowSI.magnitude
		
	# DOE-2	infiltration methodology
	NewInfObject.Constant_Term_Coefficient = 0
	NewInfObject.Velocity_Term_Coefficient = 0.244
	
if __name__ == '__main':
	CreateAndAssignInfiltration(idf_file,*args)