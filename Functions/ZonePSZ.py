from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Zone:Unitary a zone for a PSZ system.
# Important Notes:
#				- Make sure that there is a "IntermittentFan" Schedule in the model always set to 0 (cycling fan).
# Arg. Values: 
#				- NbZone: Any > 1.
#				- ZoneNames: Any valid zone name.
#				- System: Any valid template VRF system.
#				- Thermostat: Any valid thermostat.
#				- OACFMperFt2: Any > 0.

def ZonePSZ(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	ZoneNames = []
	NbZone = int(args[0][0])	
	if NbZone == 1:
		ZoneNames.append(args[0][1])
	else:
		for i in range(1,NbZone+1):
			ZoneNames.append(args[0][i])
	System = args[0][NbZone+1]	
	Thermostat = args[0][NbZone+2]
	OACFMperFt2 = args[0][NbZone+3]		
	
	# Conversion from W/Cfm to m3/second
	OACFMperFt2 = float(OACFMperFt2)
	OACFMperFt2IP = OACFMperFt2*ureg.foot**3/(ureg.minute*ureg.foot**2)
	OACFMperFt2SI = OACFMperFt2IP.to(ureg.meter**3/(ureg.second*ureg.meter**2))	
	
	# Create zone for PSZ
	ZonePSZ = idf_file.newidfobject("HVACTEMPLATE:ZONE:UNITARY")
	ZonePSZ.Zone_Name = ZoneNames[0]
	ZonePSZ.Template_Unitary_System_Name = System
	ZonePSZ.Template_Thermostat_Name = Thermostat
	ZonePSZ.Zone_Heating_Sizing_Factor = 1.25
	ZonePSZ.Zone_Cooling_Sizing_Factor = 1.15
	ZonePSZ.Outdoor_Air_Method = "Flow/Area"
	ZonePSZ.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = OACFMperFt2SI.magnitude
	ZonePSZ.Zone_Cooling_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZonePSZ.Zone_Cooling_Design_Supply_Air_Temperature_Difference = 11.1
	ZonePSZ.Zone_Heating_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZonePSZ.Zone_Heating_Design_Supply_Air_Temperature_Difference = 11.1	
	
	# Copy the object if more than one zone have been specified
	if len(ZoneNames) > 1:
		for i in range(1,len(ZoneNames)):
			ZonePSZ = idf_file.copyidfobject(ZoneVRF)
			idf_file.idfobjects["HVACTEMPLATE:ZONE:UNITARY"][-1].Zone_Name = ZoneNames[i]		
	
if __name__ == '__main':
	ZonePSZ(idf_file,*args)	