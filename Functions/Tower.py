from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create using the HVACTemplate:Plant:Tower a cooling tower.
# Arg. Values: 
#				- Type: SingleSpeed or TwoSpeed.
#				- LoopType: HotWater, MixedWater.

def Tower(idf_file,*args):
	# Object and variables initialization
	Type = args[0][0]
	LoopType = args[0][1]
	
	Tower = idf_file.newidfobject("HVACTEMPLATE:PLANT:TOWER")
	Tower.Name = "Tower"
	Tower.Tower_Type = Type
	Tower.Template_Plant_Loop_Type = LoopType

if __name__ == '__main':
	Tower(idf_file,*args)	