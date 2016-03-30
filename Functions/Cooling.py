from eppy import modeleditor
from eppy.modeleditor import IDF

def Cooling(idf_file,Cooling):
	ScheduleObjects = idf_file.idfobjects["SCHEDULE:CONSTANT"]
	for i in range(0,len(ScheduleObjects)):
		if ScheduleObjects[i].Name == "Always78":
			if Cooling == "Y":
				ScheduleObjects[i].Hourly_Value = 25.6
			else:
				ScheduleObjects[i].Hourly_Value = 50

if __name__ == '__main':
	Cooling(idf_file,Cooling)