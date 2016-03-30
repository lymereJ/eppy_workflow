from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Set the FAN:ZONEEXHAUST pressure rise based on the fan power (W/CFM)
# Arg. Values: Any

def FanEff(idf_file,FanEff):
	ureg = UnitRegistry()
	FanZoneExhaustObjects = idf_file.idfobjects["FAN:ZONEEXHAUST"]
	for i in range(0,len(FanZoneExhaustObjects)):
		FanEff = float(FanEff)
		VentilationFlowinIP = FanEff*ureg.watt/((ureg.foot**3)/ureg.minute)
		VentilationFlowinSI = VentilationFlowinIP.to(ureg.watt/((ureg.meter**3)/ureg.second))
		FanZoneExhaustObjects[i].Pressure_Rise = VentilationFlowinSI.magnitude * FanZoneExhaustObjects[i].Fan_Total_Efficiency

if __name__ == '__main':
	FanEff(idf_file,FanEff)