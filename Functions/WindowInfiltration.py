from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Thermal comfort study in the PNW on a apartment unit test cell
# Function: Change the Air Leakage (AL) for the window(s)
# Arg. Values: Any

def WindowInfiltration(idf_file,WindowInfiltration):
	ureg = UnitRegistry()
	WindowOpeningObjects = idf_file.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]
	WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
	WindowAFNObjects = idf_file.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]

	for j in range(0,len(WindowObjects)):
		WindowArea = WindowObjects[j].area
		WindowHeight = WindowObjects[j].Vertex_1_Zcoordinate - WindowObjects[j].Vertex_2_Zcoordinate
		WindowWidth = WindowObjects[j].area / WindowHeight
		WindowPerimeter = 2 * (WindowHeight + WindowWidth)
		for k in range(0,len(WindowAFNObjects)):
			if WindowAFNObjects[k].Surface_Name == WindowObjects[j].Name:
				for i in range(0,len(WindowOpeningObjects)):
					if WindowAFNObjects[k].Leakage_Component_Name == WindowOpeningObjects[i].Name:
						# AL is given in cfm/ft2 of window
						AL = float(WindowInfiltration)*ureg.foot**3/(ureg.minute*ureg.foot**2)
						AL = AL.to(ureg.meter**3/(ureg.second*ureg.meter**2))
						AL = AL.magnitude		
						
						# rho is in kg/m3 and corresponds to the air state @ test procedure: 1013 hPa, 50% RH, 21C DB
						rho = 1.1942 
						
						# delta in Pa
						deltaP = 75
						
						Exponent = WindowOpeningObjects[i].Air_Mass_Flow_Exponent_When_Opening_is_Closed
						
						# Window perimeter is adjusted for the average number of windows ~2 per facade
						WindowPerimeterAdjusted = WindowPerimeter * 2
						
						# (Mass Flow Rate) = (Air Mass Flow Coefficient) * deltaP ^ (Air Mass Flow Exponent)
						# (Air Mass Flow Coefficient) is per meter of crack length i.e. = (Air Mass Flow Coefficient) / Window Perimeter
						# (Mass Flow Rate) = AL * rho * WindowArea
						WindowOpeningObjects[i].Air_Mass_Flow_Coefficient_When_Opening_is_Closed =  (AL * rho * WindowArea * WindowPerimeterAdjusted) / (deltaP ** Exponent)
		
if __name__ == '__main':
	WindowInfiltration(idf_file,WindowInfiltration)