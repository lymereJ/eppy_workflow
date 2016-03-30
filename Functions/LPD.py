from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

def LPD(idf_file,LPD):
	ureg = UnitRegistry()
	LightsObjects = idf_file.idfobjects["LIGHTS"]
	for i in range(0,len(LightsObjects)):
		LPD = float(LPD)
		LPDinIP = LPD*ureg.watt/ureg.foot**2
		LPDinSI = LPDinIP.to((ureg.watt)/ureg.meter**2)
		LightsObjects[i].Watts_per_Zone_Floor_Area = LPDinSI.magnitude

if __name__ == '__main':
	LPD(idf_file,LPD)