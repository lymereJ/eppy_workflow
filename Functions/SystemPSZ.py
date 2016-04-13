from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:System:UnitarySystem a PSZ unit.
# Important Notes:
#				- Make sure that there is a "IntermittentFan" Schedule in the model always set to 0 (cycling fan).
# Arg. Values: 
#				- SystemName: Any.
#				- ControlZone: Any available zones.
#				- SupplyFanOperation: Intermittent or Continuous.
#				- SupplyFanEff: Any > 0.
#				- ClgCoilType: SingleSpeedDX, TwoSpeedDX.
#				- ClgEER: Any > 0.
#				- HtgCoilType: Gas, SingleSpeedDXHeatPumpAirSource.
#				- HtgCOP: Any > 0.
#				- MinOA: Any > 0.
#				- Economizer: NoEconomizer, FixedDryBulb.

def SystemPSZ(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	SystemName	= args[0][0]
	ControlZone	= args[0][1]
	SupplyFanOperation = args[0][2]
	SupplyFanEff = args[0][3]
	ClgCoilType	= args[0][4]
	ClgEER	= args[0][5]
	HtgCoilType	= args[0][6]
	HtgCOP	= args[0][7]
	MinOA	= args[0][8]
	Economizer	= args[0][9]
	
	# Fan efficiency calculation and conversion
	SupplyFanEff = float(SupplyFanEff)
	SupplyFanEffIP = SupplyFanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
	SupplyFanEffSI = SupplyFanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))	

	# Conversion from Cfm to m3/second
	if MinOA <> "autosize":
		MinOA = float(MinOA)
		MinOAIP = MinOA*ureg.foot**3/ureg.minute
		MinOASI = MinOAIP.to(ureg.meter**3/ureg.second)	
	
	if SupplyFanOperation == "Continuous":
		ClgCOP = ((1/3.413)+0.012167)/((1/float(ClgEER))-0.012167)	
	else:
		ClgCOP = float(ClgEER) / 3.413
		
	if SupplyFanOperation == "Continuous" and HtgCoilType <> "Gas":
		HtgCoilCOP = ((1/3.413)-0.012167)/((1/(float(ClgEER)*3.412)-0.012167))	
		
	# Create new PSZ system
	SystemPSZ = idf_file.newidfobject("HVACTEMPLATE:SYSTEM:UNITARYSYSTEM")
	SystemPSZ.Name = SystemName
	SystemPSZ.Control_Type = "Load"
	SystemPSZ.Control_Zone_or_Thermostat_Location_Name = ControlZone
	if SupplyFanOperation == "Intermittent":
		SystemPSZ.Supply_Fan_Operating_Mode_Schedule_Name = "IntermittentFan"
	SystemPSZ.Supply_Fan_Total_Efficiency = 0.65
	SystemPSZ.Supply_Fan_Delta_Pressure = SupplyFanEffSI.magnitude * SystemPSZ.Supply_Fan_Total_Efficiency
	SystemPSZ.Cooling_Coil_Type = ClgCoilType
	if ClgCoilType == "TwoSpeedDX":
		SystemPSZ.Number_of_Speeds_for_Cooling = 2
	SystemPSZ.Cooling_Design_Supply_Air_Temperature = 12.8
	SystemPSZ.DX_Cooling_Coil_Gross_Rated_COP = ClgCOP
	SystemPSZ.Heating_Coil_Type = HtgCoilType
	SystemPSZ.Heating_Design_Supply_Air_Temperature = 33.33
	if HtgCoilType <> "Gas":
		SystemPSZ.Heat_Pump_Heating_Coil_Gross_Rated_COP = HtgCOP
	SystemPSZ.Supplemental_Heating_or_Reheat_Coil_Type = "Electric"
	if MinOA <> "autosize":
		SystemPSZ.Minimum_Outdoor_Air_Flow_Rate = MinOASI.magnitude
	SystemPSZ.Economizer_Type = Economizer
	SystemPSZ.Economizer_Maximum_Limit_DryBulb_Temperature = 23.8
	

if __name__ == '__main':
	SystemPSZ(idf_file,*args)