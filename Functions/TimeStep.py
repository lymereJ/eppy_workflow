from eppy import modeleditor
from eppy.modeleditor import IDF

def TimeStep(idf_file,TimeStep):
	TimeStepObjects = idf_file.idfobjects["TIMESTEP"]
	for i in range(0,len(TimeStepObjects)):
		TimeStepObjects[i].Number_of_Timesteps_per_Hour = TimeStep

if __name__ == '__main':
	TimeStep(idf_file,TimeStep)