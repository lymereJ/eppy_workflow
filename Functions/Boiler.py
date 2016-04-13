from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Plant:Boiler a boiler.
# Arg. Values: 
#				- Type: HotWaterBoiler, CondensingHotWaterBoiler or DistrictHotWater.
#				- Fuel: Electricity or NaturalGas.
#				- Efficiency: Any > 0.
#				- LoopType: HotWater, MixedWater.

def Boiler(idf_file,*args):
	# Define the Unit Registry used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	Type = args[0][0]
	Fuel = args[0][1]
	Efficiency = args[0][2]
	WaterType = args[0][3]
	
	Boiler = idf_file.newidfobject("HVACTEMPLATE:PLANT:BOILER")
	Boiler.Name = "Boiler"
	Boiler.Boiler_Type = Type
	Boiler.Efficiency = Efficiency
	Boiler.Fuel_Type = Fuel
	Boiler.Template_Plant_Loop_Type = WaterType
	
if __name__ == '__main':
	Boiler(idf_file,*args)	