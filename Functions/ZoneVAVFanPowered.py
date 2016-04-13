from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Zone:VAV:FanPowered, Fan powered VAV boxes.
# Important Notes:
#				- The supply air is being calculated based on a 20 degree Dt.
# Arg. Values: 
#				- NbZone: Any > 1.
#				- ZoneNames: Any valid zone name.
#				- System: Any valid system name.
#				- Thermostat: Any valid thermostat.
#				- FlowType: Series or Parallel
#				- OACFMperFt2: Any > 0.
#				- ReheatType: Electric, HotWater, or Gas.
#				- FanEff:	Any > 0.

def ZoneVAVFanPowered(idf_file,*args):
	# Define the Unit Registry used for unit conversion
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
	FlowType = args[0][NbZone+3]
	OACFMperFt2 = args[0][NbZone+4]
	ReheatType = args[0][NbZone+5]
	FanEff = args[0][NbZone+6]
	
	# Conversion from W/Cfm to m3/second
	OACFMperFt2 = float(OACFMperFt2)
	OACFMperFt2IP = OACFMperFt2*ureg.foot**3/(ureg.minute*ureg.foot**2)
	OACFMperFt2SI = OACFMperFt2IP.to(ureg.meter**3/(ureg.second*ureg.meter**2))
	FanEff = float(FanEff)
	FanEffIP = FanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
	FanEffSI = FanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))
	
	# Create First Object
	ZoneVAVFPB = idf_file.newidfobject("HVACTEMPLATE:ZONE:VAV:FANPOWERED")
	ZoneVAVFPB.Zone_Name = ZoneNames[0]
	ZoneVAVFPB.Template_VAV_System_Name = System
	ZoneVAVFPB.Template_Thermostat_Name = Thermostat
	ZoneVAVFPB.Zone_Heating_Sizing_Factor = 1.25
	ZoneVAVFPB.Zone_Cooling_Sizing_Factor = 1.15
	ZoneVAVFPB.Primary_Supply_Air_Minimum_Flow_Fraction = 0.3
	ZoneVAVFPB.Flow_Type = FlowType
	ZoneVAVFPB.Outdoor_Air_Method = "Flow/Area"
	ZoneVAVFPB.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = OACFMperFt2SI.magnitude
	ZoneVAVFPB.Reheat_Coil_Type = ReheatType
	ZoneVAVFPB.Fan_Total_Efficiency = 0.65
	# Default ASHRAE sizing method: delta-t = 20F
	ZoneVAVFPB.Fan_Delta_Pressure = FanEffSI.magnitude * ZoneVAVFPB.Fan_Total_Efficiency
	ZoneVAVFPB.Zone_Cooling_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZoneVAVFPB.Zone_Cooling_Design_Supply_Air_Temperature_Difference = 11.1
	ZoneVAVFPB.Zone_Heating_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZoneVAVFPB.Zone_Heating_Design_Supply_Air_Temperature_Difference = 11.1

	# Copy the object if more than one zone have been specified
	if len(ZoneNames) > 1:
		for i in range(1,len(ZoneNames)):
			NewZoneVAVFPB = idf_file.copyidfobject(ZoneVAVFPB)
			idf_file.idfobjects["HVACTEMPLATE:ZONE:VAV:FANPOWERED"][-1].Zone_Name = ZoneNames[i]
	
if __name__ == '__main':
	ZoneVAVFanPowered(idf_file,*args)