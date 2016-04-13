from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Set the timestep
# Arg. Values: Any

def TimeStep(idf_file,*args):
	TimeStep = args[0][0]
	TimeStepObjects = idf_file.idfobjects["TIMESTEP"]
	if len(TimeStepObjects) == 0:
		TimeStepObject = idf_file.newidfobject("TIMESTEP")
		TimeStepObject.Number_of_Timesteps_per_Hour = TimeStep
	else:
		for i in range(0,len(TimeStepObjects)):
			TimeStepObjects[i].Number_of_Timesteps_per_Hour = TimeStep
	
if __name__ == '__main':
	TimeStep(idf_file,*args)