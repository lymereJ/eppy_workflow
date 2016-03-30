from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

def EPD(idf_file,EPD):
	ureg = UnitRegistry()
	ElectricEquipmentObjects = idf_file.idfobjects["ELECTRICEQUIPMENT"]
	for i in range(0,len(ElectricEquipmentObjects)):
		EPD = float(EPD)
		EPDinIP = EPD*ureg.watt/ureg.foot**2
		EPDinSI = EPDinIP.to((ureg.watt)/ureg.meter**2)
		ElectricEquipmentObjects[i].Watts_per_Zone_Floor_Area = EPDinSI.magnitude

if __name__ == '__main':
	EPD(idf_file,EPD)