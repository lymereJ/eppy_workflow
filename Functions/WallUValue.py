from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

def WallUValue(idf_file,WallUValue):
	ureg = UnitRegistry()
	ConstructionObjects = idf_file.idfobjects["CONSTRUCTION"]
	MaterialObjects = idf_file.idfobjects["MATERIAL"]
	ConstructionRVal = 0
	for i in range(0,len(ConstructionObjects)):
		if ConstructionObjects[i].Name == "Exterior Wall Construction":
			for j in range(1,len(ConstructionObjects[i].fieldnames)):
				for k in range (0,len(MaterialObjects)):
					if MaterialObjects[k].Name == ConstructionObjects[i].fieldnames[j] and MaterialObjects[k].Name <> "Wall Insulation" :
						ConstructionRVal = ConstructionRVal + (MaterialObjects[k].Thickness / MaterialObjects[k].Conductivity)
					elif MaterialObjects[k].Name == "Wall Insulation":
						CondIns = MaterialObjects[k].Conductivity
	
	ConstructionRVal = ConstructionRVal*(ureg.meter**2)*ureg.degK/ureg.watt
	ConstructionRVal = ConstructionRVal.to(ureg.hour*(ureg.foot**2)*ureg.delta_degF/ureg.btu)
	ConstructionRVal = ConstructionRVal.magnitude
	ConstructionRVal = ConstructionRVal + 0.680 + 0.21 + 1
	ConstructionRVal = ConstructionRVal*ureg.hour*(ureg.foot**2)*ureg.delta_degF/ureg.btu
	ConstructionRVal = ConstructionRVal.to((ureg.meter**2)*ureg.degK/ureg.watt)
	ConstructionRVal = ConstructionRVal.magnitude
	WallUValue = float(WallUValue)*ureg.btu/(ureg.hour*(ureg.foot**2)*ureg.delta_degF)
	WallUValue = WallUValue.to(ureg.watt/((ureg.meter**2)*ureg.degK))
	WallUValue = WallUValue.magnitude
	
	RValIns = (1/WallUValue) - ConstructionRVal
	ThickIns = RValIns * CondIns
	
	for l in range (0,len(MaterialObjects)):
		if MaterialObjects[l].Name == "Wall Insulation":
			MaterialObjects[l].Thickness = ThickIns

if __name__ == '__main':
	WallUValue(idf_file,WallUValue)