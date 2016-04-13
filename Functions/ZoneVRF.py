from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Zone:VRF a VRF indoor unit.
# Important Notes:
#				- Make sure that there is a "IntermittentFan" Schedule in the model always set to 0 (cycling fan).
# Arg. Values: 
#				- NbZone: Any > 1.
#				- ZoneNames: Any valid zone name.
#				- System: Any valid template VRF system.
#				- Thermostat: Any valid thermostat.
#				- OACFMperFt2: Any > 0.
#				- FanEff: Any > 0.
#				- DOAS: Yes or No.
#				- DOASSystem: Any available DOAS system.

def ZoneVRF(idf_file,*args):
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
	FanEff = args[0][NbZone+4]	
	DOAS = args[0][NbZone+5]
	if DOAS == "Yes":
		DOASSystem = args[0][NbZone+6]

	# Conversion from W/Cfm to m3/second
	OACFMperFt2 = float(OACFMperFt2)
	OACFMperFt2IP = OACFMperFt2*ureg.foot**3/(ureg.minute*ureg.foot**2)
	OACFMperFt2SI = OACFMperFt2IP.to(ureg.meter**3/(ureg.second*ureg.meter**2))
	FanEff = float(FanEff)
	FanEffIP = FanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
	FanEffSI = FanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))	
	
	ZoneVRF = idf_file.newidfobject("HVACTEMPLATE:ZONE:VRF")
	ZoneVRF.Zone_Name = ZoneNames[0]
	ZoneVRF.Template_VRF_System_Name = System
	ZoneVRF.Template_Thermostat_Name = Thermostat
	ZoneVRF.Zone_Heating_Sizing_Factor = 1.25
	ZoneVRF.Zone_Cooling_Sizing_Factor = 1.15
	ZoneVRF.Outdoor_Air_Method = "Flow/Area"
	ZoneVRF.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = OACFMperFt2SI.magnitude
	ZoneVRF.Supply_Fan_Operating_Mode_Schedule_Name = "IntermittentFan"
	ZoneVRF.Supply_Fan_Total_Efficiency = 0.65
	ZoneVRF.Supply_Fan_Delta_Pressure = FanEffSI.magnitude * ZoneVRF.Supply_Fan_Total_Efficiency
	ZoneVRF.Zone_Cooling_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZoneVRF.Zone_Cooling_Design_Supply_Air_Temperature_Difference = 11.1
	ZoneVRF.Zone_Heating_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZoneVRF.Zone_Heating_Design_Supply_Air_Temperature_Difference = 11.1
	if DOAS == "Yes":
		ZoneVRF.Dedicated_Outdoor_Air_System_Name = DOASSystem

	# Copy the object if more than one zone have been specified
	if len(ZoneNames) > 1:
		for i in range(1,len(ZoneNames)):
			NewZoneVRF = idf_file.copyidfobject(ZoneVRF)
			idf_file.idfobjects["HVACTEMPLATE:ZONE:VRF"][-1].Zone_Name = ZoneNames[i]	
	

if __name__ == '__main':
	ZoneVRF(idf_file,*args)	