from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Plant:HotWaterLoop a hot water loop.
# Arg. Values: 
#				- Name: Any.
#				- OAReset: Yes or No.
#				- LoopDT: Any > 0.
#				- PumpCfg: ConstantFlow or VariableFlow.
#				- PumpHead: Any > 0.
#				- PumpType: SinglePump, PumpPerTowerOrBoiler, TwoHeaderedPumps, ..., FiveHeaderedPumps.

def HotWaterLoop(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	Name = args[0][0]
	OAReset = args[0][1]
	LoopDT = args[0][2]
	PumpCfg = args[0][3]
	PumpHead = args[0][4]
	PumpType = args[0][5]
	
	# Conversion from F to C
	LoopDT = float(LoopDT)
	LoopDTIP = LoopDT*ureg.delta_degF
	LoopDTSI = LoopDTIP.to(ureg.delta_degC)
	
	# Conversion from ftH2O to Pa
	PumpHead = float(PumpHead)
	PumpHeadIP = PumpHead*ureg.ftH2O
	PumpHeadSI = PumpHeadIP.to(ureg.Pa)
	
	# Create new hot water loop
	HotWaterLoop = idf_file.newidfobject("HVACTEMPLATE:PLANT:HOTWATERLOOP")
	HotWaterLoop.Name = Name
	if OAReset == "Yes":
		HotWaterLoop.Hot_Water_Setpoint_Reset_Type = "OutdoorAirTemperatureReset"
		HotWaterLoop.Hot_Water_Setpoint_at_Outdoor_DryBulb_Low = 82.2
		HotWaterLoop.Hot_Water_Reset_Outdoor_DryBulb_Low = -6.7
		HotWaterLoop.Hot_Water_Setpoint_at_Outdoor_DryBulb_High = 65.6
		HotWaterLoop.Hot_Water_Reset_Outdoor_DryBulb_Low = -10
	else:
		HotWaterLoop.Hot_Water_Setpoint_Reset_Type = "None"
	HotWaterLoop.Hot_Water_Pump_Configuration = PumpCfg
	HotWaterLoop.Hot_Water_Pump_Rated_Head = PumpHeadSI.magnitude
	HotWaterLoop.Hot_Water_Pump_Type = PumpType
	HotWaterLoop.Loop_Design_Delta_Temperature = LoopDTSI.magnitude
	
if __name__ == '__main':
	HotWaterLoop(idf_file,*args)