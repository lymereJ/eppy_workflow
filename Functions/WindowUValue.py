from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

def WindowUValue(idf_file,WindowUValue):
	ureg = UnitRegistry()
	WindowObjects = idf_file.idfobjects["WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM"]
	for i in range(0,len(WindowObjects)):
		WindowUValue = float(WindowUValue)
		WindowUValueIP = WindowUValue*ureg.btu/(ureg.hour*(ureg.foot**2)*ureg.delta_degF)
		WindowUValueSI = WindowUValueIP.to((ureg.watt/ureg.meter**2/ureg.degK))
		WindowObjects[i].UFactor = WindowUValueSI.magnitude

if __name__ == '__main':
	WindowUValue(idf_file,WindowUValue)