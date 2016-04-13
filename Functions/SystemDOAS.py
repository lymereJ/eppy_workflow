from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:System:DedicatedOutdoorAir a DOAS system.
# Important Notes:
#				- .
# Arg. Values: 
#				- SystemName: Any.
#				- SupplyFanEff: Any > 0.
#				- ClgCoilType: ChilledWater, TwoSpeedDX
#				- ClgSetpoint: Any > 0.
#				- ClgEER: Any > 0.
#				- HtgCoilType: HotWater, Gas or Electric.
#				- HtgSetpoint: Any > 0.
#				- HeatRec: None, Sensible or Enthalpy.
#				- HeatRecEff: 1 > Any > 0.

def SystemDOAS(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	SystemName = args[0][0]
	SupplyFanEff = args[0][1]
	ClgCoilType = args[0][2]
	ClgSetpoint = args[0][3]
	ClgEER = args[0][4]
	HtgCoilType = args[0][5]
	HtgSetpoint = args[0][6]
	HeatRec = args[0][7]
	HeatRecEff = args[0][8]
	
	# Fan efficiency conversion
	SupplyFanEff = float(SupplyFanEff)
	SupplyFanEffIP = SupplyFanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
	SupplyFanEffSI = SupplyFanEffIP.to(ureg.watt/((ureg.meter**3)/ureg.second))	
	
	# Conversion F to C
	Clg = ureg.Quantity
	ClgSetpointIP = Clg(float(ClgSetpoint), ureg.degF)
	ClgSetpointSI = ClgSetpointIP.to('degC')	
	
	Htg = ureg.Quantity
	if HtgCoilType <> "None":
		HtgSetpointIP = Htg(float(HtgSetpoint), ureg.degF)
		HtgSetpointSI = HtgSetpointIP.to('degC')	

	# Create new DOAS system
	SystemDOAS = idf_file.newidfobject("HVACTEMPLATE:SYSTEM:DEDICATEDOUTDOORAIR")
	SystemDOAS.Name = SystemName
	SystemDOAS.Supply_Fan_Total_Efficiency = 0.65
	SystemDOAS.Supply_Fan_Delta_Pressure = SupplyFanEffSI.magnitude * SystemDOAS.Supply_Fan_Total_Efficiency	
	SystemDOAS.Cooling_Coil_Type = ClgCoilType
	SystemDOAS.Cooling_Coil_Design_Setpoint = ClgSetpointSI.magnitude
	if ClgCoilType <> "None":
		SystemDOAS.DX_Cooling_Coil_Gross_Rated_COP = float(ClgEER) / 3.413
	else:
		SystemDOAS.Supply_Fan_Placement
	SystemDOAS.Heating_Coil_Type = HtgCoilType
	if HtgCoilType <> "None":
		SystemDOAS.Heating_Coil_Design_Setpoint = HtgSetpointSI.magnitude
	SystemDOAS.Heat_Recovery_Type = HeatRec
	if HeatRec <> "None":
		SystemDOAS.Heat_Recovery_Sensible_Effectiveness = HeatRecEff
		SystemDOAS.Heat_Recovery_Latent_Effectiveness = HeatRecEff
	
	
if __name__ == '__main':
	SystemDOAS(idf_file,*args)	