from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:System:VRF a VRF outdoor unit.
# Important Notes:
#				- The template uses the older VRF EnergyPlus model.
# Arg. Values: 
#				- SystemName: Any.
#				- ClgEER: Any > 0.
#				- HtgCOP: Any > 0.
#				- MasterThermostatZone: Any available zone in the model.
#				- LoadPriority: MasterThermostatPriority, LoadPriority, ZonePriority or ThermostatOffsetPriority
#				- HeatRec: Yes or No.
#				- HorizontalPipeLength: Any > 0.
#				- VerticalPipeLength Any > 0.
#				- CondenserType: AirCooled or WaterCooled.
#				- DefrostType: Resistive or ReverseCycle

def SystemVRF(idf_file,*args):
	# Define the Unit Registry used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	SystemName = args[0][0]
	ClgEER = args[0][1]
	HtgCOP = args[0][2]
	MasterThermostatZone = args[0][3]
	LoadPriority = args[0][4]
	HeatRec = args[0][5]
	HorizontalPipeLength = args[0][6]
	VerticalPipeLength = args[0][7]
	CondenserType = args[0][8]
	DefrostType = args[0][9]
	
	# Conversion from ft to m
	HorizontalPipeLength = float(HorizontalPipeLength)
	HorizontalPipeLengthIP = HorizontalPipeLength*ureg.foot
	HorizontalPipeLengthSI = HorizontalPipeLengthIP.to(ureg.meter)
	
	VerticalPipeLength = float(VerticalPipeLength)
	VerticalPipeLengthIP = VerticalPipeLength*ureg.foot
	VerticalPipeLengthSI = VerticalPipeLengthIP.to(ureg.meter)	
	
	# Create new VRF system
	SystemVRF = idf_file.newidfobject("HVACTEMPLATE:SYSTEM:VRF")
	SystemVRF.Name = SystemName
	SystemVRF.Gross_Rated_Cooling_COP = float(ClgEER) / 3.413
	SystemVRF.Gross_Rated_Heating_COP = HtgCOP
	if CondenserType == "WaterCooled":
		SystemVRF.Maximum_Outdoor_Temperature_in_Heating_Mode = 45
	SystemVRF.Zone_Name_for_Master_Thermostat_Location = MasterThermostatZone
	SystemVRF.Master_Thermostat_Priority_Control_Type = LoadPriority
	SystemVRF.Heat_Pump_Waste_Heat_Recovery = HeatRec
	SystemVRF.Equivalent_Piping_Length_used_for_Piping_Correction_Factor_in_Cooling_Mode = HorizontalPipeLengthSI.magnitude
	SystemVRF.Vertical_Height_used_for_Piping_Correction_Factor = VerticalPipeLengthSI.magnitude
	SystemVRF.Equivalent_Piping_Length_used_for_Piping_Correction_Factor_in_Heating_Mode = HorizontalPipeLengthSI.magnitude
	SystemVRF.Defrost_Strategy = DefrostType
	SystemVRF.Condenser_Type = CondenserType
	
if __name__ == '__main':
	SystemVRF(idf_file,*args)	