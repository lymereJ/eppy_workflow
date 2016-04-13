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
#				- OACFMperFt2: Any > 0.
#				- ReheatType: Electric, HotWater, or Gas.

def ZoneVAV(idf_file,*args):
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
	ReheatType = args[0][NbZone+4]
	SurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	
	# Conversion from W/Cfm to m3/second
	OACFMperFt2 = float(OACFMperFt2)
	OACFMperFt2IP = OACFMperFt2*ureg.foot**3/(ureg.minute*ureg.foot**2)
	OACFMperFt2SI = OACFMperFt2IP.to(ureg.meter**3/(ureg.second*ureg.meter**2))
	
	# Conversion from cfm/ft2 to m3/s
	MinFlowRate = 0.4
	MinFlowRateIP = MinFlowRate*ureg.foot**3/(ureg.minute*ureg.foot**2)
	MinFlowRateSI = MinFlowRateIP.to(ureg.meter**3/(ureg.second*ureg.meter**2))	
	
	# Create First Object
	ZoneVAV = idf_file.newidfobject("HVACTEMPLATE:ZONE:VAV")
	ZoneVAV.Zone_Name = ZoneNames[0]
	ZoneVAV.Template_VAV_System_Name = System
	ZoneVAV.Template_Thermostat_Name = Thermostat
	ZoneVAV.Zone_Heating_Sizing_Factor = 1.25
	ZoneVAV.Zone_Cooling_Sizing_Factor = 1.15
	ZoneVAV.Zone_Minimum_Air_Flow_Input_Method = "FixedFlowRate"
	ZoneArea = 0
	for i in range(0,len(SurfaceObjects)):
		if SurfaceObjects[i].Zone_Name == ZoneNames[0] and SurfaceObjects[i].Surface_Type == "Floor":
			ZoneArea = ZoneArea + SurfaceObjects[i].area
	ZoneVAV.Fixed_Minimum_Air_Flow_Rate = MinFlowRateSI.magnitude * ZoneArea
	ZoneVAV.Outdoor_Air_Method = "Flow/Area"
	ZoneVAV.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = OACFMperFt2SI.magnitude
	ZoneVAV.Reheat_Coil_Type = ReheatType
	ZoneVAV.Zone_Cooling_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZoneVAV.Zone_Cooling_Design_Supply_Air_Temperature_Difference = 11.1
	ZoneVAV.Zone_Heating_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	ZoneVAV.Zone_Heating_Design_Supply_Air_Temperature_Difference = 11.1

	# Copy the object if more than one zone have been specified
	if len(ZoneNames) > 1:
		for i in range(1,len(ZoneNames)):
			NewZoneVAV = idf_file.copyidfobject(ZoneVAV)
			NewZoneVAV = idf_file.idfobjects["HVACTEMPLATE:ZONE:VAV"][-1]
			NewZoneVAV.Zone_Name = ZoneNames[i]
			ZoneArea = 0
			for j in range(0,len(SurfaceObjects)):
				if SurfaceObjects[j].Zone_Name == ZoneNames[i] and SurfaceObjects[j].Surface_Type == "Floor":
					ZoneArea = ZoneArea + SurfaceObjects[i].area
			NewZoneVAV.Fixed_Minimum_Air_Flow_Rate = MinFlowRateSI.magnitude * ZoneArea
	
if __name__ == '__main':
	ZoneVAV(idf_file,*args)