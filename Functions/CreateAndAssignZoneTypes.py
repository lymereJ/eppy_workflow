from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create a ZONELIST object for the Zone Type specified as input and assign all the specified Zone to it.
# Arg. Values: 
#				- ZoneType: Any.
#				- ZoneName1...n: Any valid zone name present in the model

def CreateAndAssignZoneTypes(idf_file, *args):
	# Object and variables initialization	
	Zones = []
	ZoneType = args[0][0]
	ZoneListObjects = idf_file.idfobjects["ZONELIST"]
	ZoneListObjectIdx = 0
	
	# Retrieve the zone name
	for i in range(1,len(args[0])):
		Zones.append(args[0][i])
	
	for i in range(0,len(ZoneListObjects)):
		if ZoneListObjects[i].Name == ZoneType:
			ZoneListObjectIdx = i
	
	if ZoneListObjectIdx == 0:
		ZoneListObject = idf_file.newidfobject("ZONELIST")
		ZoneListObject.Name = ZoneType
	else:
		ZoneListObject = ZoneListObjects[ZoneListObjectIdx]
	
	for i in range(0,len(Zones)):
		ZoneListObject[ZoneListObject.fieldnames[i+2]] = Zones[i]
		
if __name__ == '__main':
	CreateAndAssignZoneTypes(idf_file,*args)