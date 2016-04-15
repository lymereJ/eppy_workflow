from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:System:PackagedVAV a packaged VAV system.
# Important Notes:
#				- TwoSpeedDX cooling coil.
# Arg. Values: 
#				- SystemName: Any.
#				- ClgEER: Any > 0.
#				- ClgSetpoint: Any > 0.
#				- ClgSetpointReset: None, Warmest, OutdoorAirTemperatureReset, WarmestTemperatureFirst.
#				- HtgSrc: None,HotWater, Electric, Gas.
#				- HtgSetpoint: Any > 0.
#				- HtgSetpointReset: None, OutdoorAirTemperatureReset.
#				- SupplyFanEff: Any > 0.
#				- MinOA: Any > 0 or autosize.
#				- Economizer: NoEconomizer, FixedDryBulb, FixedEnthalpy, DifferentialDryBulb, DifferentialEnthalpy.
#				- HeatRec: None, Sensible, or Enthalpy
#				- ReturnFan: Yes or No.
#				- FanCurve: VariableSpeedMotor, ASHRAE90.1-2004AppendixG or VariableSpeedMotorPressureReset.
#				- HeatRecEff: Any > 0. (Optional)
#				- ReturnFanEff: Any > 0. (Optional)

def SystemPkgVAV(idf_file,*args):
	# Define the Unit Registry used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	SystemName = args[0][0]
	ClgEER = args[0][1]
	ClgSetpoint = args[0][2]
	ClgSetpointReset = args[0][3]
	HtgSrc = args[0][4]
	HtgSetpoint = args[0][5]
	HtgSetpointReset = args[0][6]
	SupplyFanEff = args[0][7]
	MinOA = args[0][8]
	Economizer = args[0][9]
	HeatRec = args[0][10]
	ReturnFan = args[0][11]
	FanCurve = args[0][12]
	if HeatRec <> "None":
		HeatRecEff = args[0][13]
	if ReturnFan == "Yes":
		ReturnFanEff = args[0][14]
	
	# Conversion of the Cooling EER to Cooling COP; According to ASHRAE 90.1 Appendix G, since the fan will run continuously the fan power should be modeled separetly of the cooling efficiency rating
	ClgCOP = ((1/3.413)+0.012167)/((1/float(ClgEER))-0.012167)
	
	# Conversion of minimum OA from cfm to m3/s
	if MinOA <> "autosize":
		MinOA = float(MinOA)
		MinOAIP = MinOA*ureg.foot**3/ureg.minute
		MinOASI = MinOAIP.to(ureg.meter**3/ureg.second)
	
	# Conversion F to C
	Clg = ureg.Quantity
	ClgSetpointIP = Clg(float(ClgSetpoint), ureg.degF)
	ClgSetpointSI = ClgSetpointIP.to('degC')
	
	Htg = ureg.Quantity
	HtgSetpointIP = Htg(float(HtgSetpoint), ureg.degF)
	HtgSetpointSI = HtgSetpointIP.to('degC')	
	
	# Fan efficiency conversion
	SupplyFanEff = float(SupplyFanEff)
	SupplyFanEffIP = SupplyFanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
	SupplyFanEffSI = SupplyFanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))
	if ReturnFan == "Yes":
		ReturnFanEff = float(ReturnFanEff)
		ReturnFanEffIP = ReturnFanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
		ReturnFanEffSI = ReturnFanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))
	
	# Create System Object
	PkgVAVSystem = idf_file.newidfobject("HVACTEMPLATE:SYSTEM:PACKAGEDVAV")
	PkgVAVSystem.Name = SystemName
	PkgVAVSystem.Supply_Fan_Total_Efficiency = 0.65
	PkgVAVSystem.Supply_Fan_Delta_Pressure = SupplyFanEffSI.magnitude * PkgVAVSystem.Supply_Fan_Total_Efficiency
	PkgVAVSystem.Cooling_Coil_Design_Setpoint = ClgSetpointSI.magnitude
	PkgVAVSystem.Cooling_Coil_Gross_Rated_COP = ClgCOP
	PkgVAVSystem.Heating_Coil_Type = HtgSrc
	PkgVAVSystem.Heating_Coil_Design_Setpoint = HtgSetpointSI.magnitude
	if MinOA <> "autosize":
		PkgVAVSystem.Minimum_Outdoor_Air_Flow_Rate = MinOASI.magnitude
	else:
		PkgVAVSystem.Minimum_Outdoor_Air_Flow_Rate = "autosize"
	PkgVAVSystem.Minimum_Outdoor_Air_Control_Type = "FixedMinimum"
	PkgVAVSystem.Economizer_Type = Economizer
	# Default for Seattle, WA; climate zone 4C	
	PkgVAVSystem.Economizer_Maximum_Limit_DryBulb_Temperature = 23.8
	PkgVAVSystem.Economizer_Maximum_Limit_Enthalpy = 47257
	PkgVAVSystem.Heat_Recovery_Type = HeatRec
	if HeatRec <> "None":
		PkgVAVSystem.Sensible_Heat_Recovery_Effectiveness = HeatRecEff
		PkgVAVSystem.Latent_Heat_Recovery_Effectiveness = HeatRecEff
	PkgVAVSystem.Return_Fan = ReturnFan
	if ReturnFan == "Yes":
		PkgVAVSystem.Return_Fan_Total_Efficiency = 0.65
		PkgVAVSystem.Return_Fan_Delta_Pressure = ReturnFanEffSI.magnitude * PkgVAVSystem.Return_Fan_Total_Efficiency
	PkgVAVSystem.Supply_Fan_PartLoad_Power_Coefficients = FanCurve
	PkgVAVSystem.Cooling_Coil_Setpoint_Reset_Type = ClgSetpointReset
	PkgVAVSystem.Heating_Coil_Setpoint_Reset_Type = HtgSetpointReset
	
if __name__ == '__main':
	SystemPkgVAV(idf_file,*args)