from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: When using the VentingMethod Temperature, sets the temperature when the natural ventilation is allowed
# Arg. Values: Any

def VentingTemp(idf_file,VentingTemp):
	ureg = UnitRegistry()
	ScheduleObjects = idf_file.idfobjects["SCHEDULE:COMPACT"]
	for i in range(0,len(ScheduleObjects)):
		if ScheduleObjects[i].Name == "WindowVentSched":
			Q_ = ureg.Quantity
			VentingTemp = Q_(float(VentingTemp),ureg.degF)
			VentingTemp = VentingTemp.to('degC')
			ScheduleObjects[i].Field_4 = VentingTemp.magnitude

if __name__ == '__main':
	VentingTemp(idf_file,VentingTemp)