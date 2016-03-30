from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

def InternalMass(idf_file,InternalMass):
	ureg = UnitRegistry()
	InternalMassObjects = idf_file.idfobjects["INTERNALMASS"]
	MaterialObjects = idf_file.idfobjects["MATERIAL"]
	SurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
	
	for j in range(0,len(SurfaceObjects)):
		if SurfaceObjects[j].Name == "Bottom Surface":
			ApartmentArea = SurfaceObjects[j].area
	
	for i in range(0,len(MaterialObjects)):
		if MaterialObjects[i].Name == "Furniture":
			InternalMass = float(InternalMass)*ureg.pounds/ureg.foot**2
			InternalMass = InternalMass.to(ureg.kilogram/ureg.meter**2)
			InternalMass = InternalMass.magnitude
			InternalMassObjects[0].Surface_Area = (InternalMass * ApartmentArea) / (MaterialObjects[i].Density * MaterialObjects[i].Thickness)

if __name__ == '__main':
	InternalMass(idf_file,InternalMass)