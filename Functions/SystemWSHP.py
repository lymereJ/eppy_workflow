from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Zone:WaterToAirHeatPump a water source heat pump.
# Important Notes:
#				- Make sure that there is a "IntermittentFan" Schedule in the model always set to 0 (cycling fan).
# Arg. Values: 
#				- NbZone: Any > 1.
#				- ZoneNames: Any valid zone name.
#				- Thermostat: Any valid thermostat.
#				- OACFMperFt2: Any > 0.
#				- FanEff: Any > 0.
#				- ClgEER: Any > 0.
#				- HtgCOP: Any > 0.

def WSHP(idf_file,*args):
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
	Thermostat = args[0][NbZone+1]
	OACFMperFt2 = args[0][NbZone+2]
	FanEff = args[0][NbZone+3]
	ClgEER = args[0][NbZone+4]
	HtgCOP = args[0][NbZone+5]
	
	# Conversion from W/Cfm to m3/second
	OACFMperFt2 = float(OACFMperFt2)
	OACFMperFt2IP = OACFMperFt2*ureg.foot**3/(ureg.minute*ureg.foot**2)
	OACFMperFt2SI = OACFMperFt2IP.to(ureg.meter**3/(ureg.second*ureg.meter**2))
	FanEff = float(FanEff)
	FanEffIP = FanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
	FanEffSI = FanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))
	
	WSHP = idf_file.newidfobject("HVACTEMPLATE:ZONE:WATERTOAIRHEATPUMP")
	WSHP.Zone_Name = ZoneNames[0]
	WSHP.Template_Thermostat_Name = Thermostat
	WSHP.Zone_Heating_Sizing_Factor = 1.25
	WSHP.Zone_Cooling_Sizing_Factor = 1.15
	WSHP.Outdoor_Air_Method = "Flow/Area"
	WSHP.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = OACFMperFt2SI.magnitude
	WSHP.Supply_Fan_Operating_Mode_Schedule_Name = "IntermittentFan"
	WSHP.Supply_Fan_Total_Efficiency = 0.65
	WSHP.Supply_Fan_Delta_Pressure = FanEffSI.magnitude * WSHP.Supply_Fan_Total_Efficiency
	WSHP.Cooling_Coil_Gross_Rated_COP = float(ClgEER) / 3.413
	WSHP.Heat_Pump_Heating_Coil_Gross_Rated_COP = HtgCOP
	WSHP.Zone_Cooling_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	WSHP.Zone_Cooling_Design_Supply_Air_Temperature_Difference = 11.1
	WSHP.Zone_Heating_Design_Supply_Air_Temperature_Input_Method = "TemperatureDifference"
	WSHP.Zone_Heating_Design_Supply_Air_Temperature_Difference = 11.1	
	
	# Copy the object if more than one zone have been specified
	if len(ZoneNames) > 1:
		for i in range(1,len(ZoneNames)):
			NewWSHP = idf_file.copyidfobject(WSHP)
			idf_file.idfobjects["HVACTEMPLATE:ZONE:WATERTOAIRHEATPUMP"][-1].Zone_Name = ZoneNames[i]	

if __name__ == '__main':
	WSHP(idf_file,*args)