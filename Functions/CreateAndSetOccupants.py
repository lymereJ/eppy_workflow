from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create and set occupants based on the Area/Person.
# Important Notes:
#				- The radiative fraction is an optional arguments.
# Arg. Values: 
#				- ZoneType: Any available zone type name.
#				- ScheduleName: Any available schedule name.
#				- Ft2PerPers: Any > 0.
#				- ActivityLevelSchedule: Any available schedule name.
#				- RadFrac (Optional): 1 < Any < 0.

def CreateAndSetOccupants(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	ZoneType = args[0][0]
	ScheduleName = args[0][1]	
	Ft2PerPers = args[0][2]	
	ActivityLevelSchedule = args[0][3]
	
	# Conversion from ft2/pers to m2/pers
	Ft2PerPers = float(Ft2PerPers)
	Ft2PerPersIP = Ft2PerPers*ureg.foot**2
	Ft2PerPersSI = Ft2PerPersIP.to(ureg.meter**2)
	
	People = idf_file.newidfobject("PEOPLE")
	People.Name = "Occupants-"+ZoneType
	People.Zone_or_ZoneList_Name = ZoneType
	People.Number_of_People_Schedule_Name = ScheduleName
	People.Number_of_People_Calculation_Method = "Area/Person"
	People.Zone_Floor_Area_per_Person = Ft2PerPersSI.magnitude
	People.Activity_Level_Schedule_Name = ActivityLevelSchedule
	if len(args) > 4:
		RadFrac = args[0][4]
		People.Fraction_Radiant = RadFrac
	People.Fraction_Radiant = 0.7
	People.Sensible_Heat_Fraction = 0.56
		
if __name__ == '__main':
	CreateAndSetOccupants(idf_file,*args)
