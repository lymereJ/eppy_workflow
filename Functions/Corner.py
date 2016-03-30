from eppy import modeleditor
from eppy.modeleditor import IDF

def Corner(idf_file,Corner):
	if Corner == "Y":
		BuildingSurfaceObjects = idf_file.idfobjects["BUILDINGSURFACE:DETAILED"]
		for i in range(0,len(BuildingSurfaceObjects)):
			if BuildingSurfaceObjects[i].Name == "Side Surface w/ Window":
				BuildingSurfaceObjects[i].Outside_Boundary_Condition = "Outdoors"
				BuildingSurfaceObjects[i].Outside_Boundary_Condition_Object = ""
				BuildingSurfaceObjects[i].Construction_Name = "Exterior Wall Construction"
		
		WindowObjects = idf_file.idfobjects["FENESTRATIONSURFACE:DETAILED"]
		for i in range(0,len(WindowObjects)):
			if WindowObjects[i].Name == "Side Window":
				WindowObjects[i].Surface_Type = "Window"
				WindowObjects[i].Construction_Name = "Window Construction"
				WindowObjects[i].Outside_Boundary_Condition_Object = ""
		
		
		NewWindowAFN = idf_file.newidfobject("AIRFLOWNETWORK:MULTIZONE:SURFACE")
		NewWindowAFN.Surface_Name = "Side Surface w/ Window"
		NewWindowAFN.Leakage_Component_Name = "Side Surface w/ Window ELA"
		NewWindowAFN.Ventilation_Control_Mode = "NoVent"
		
		NewWindowAFN = idf_file.newidfobject("AIRFLOWNETWORK:MULTIZONE:SURFACE")
		NewWindowAFN.Surface_Name = "Side Window"
		NewWindowAFN.Leakage_Component_Name = "WindowSideOpening"
		NewWindowAFN.Ventilation_Control_Mode = "ZoneLevel"
		NewWindowAFN.Minimum_Venting_Open_Factor = 1
		
		NewWindowAFN = idf_file.newidfobject("AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING")
		NewWindowAFN.Name = "WindowSideOpening"
		NewWindowAFN.Extra_Crack_Length_or_Height_of_Pivoting_Axis = 0
		NewWindowAFN.Number_of_Sets_of_Opening_Factor_Data = 2
		NewWindowAFN.Opening_Factor_1 = 0
		NewWindowAFN.Discharge_Coefficient_for_Opening_Factor_1 = 0.6
		NewWindowAFN.Width_Factor_for_Opening_Factor_1 = 1
		NewWindowAFN.Height_Factor_for_Opening_Factor_1 = 1
		NewWindowAFN.Start_Height_Factor_for_Opening_Factor_1 = 0
		NewWindowAFN.Opening_Factor_2 = 1
		NewWindowAFN.Discharge_Coefficient_for_Opening_Factor_2 = 0.6
		NewWindowAFN.Width_Factor_for_Opening_Factor_2 = 1
		NewWindowAFN.Height_Factor_for_Opening_Factor_2 = 1
		NewWindowAFN.Start_Height_Factor_for_Opening_Factor_2 = 0		
		
		

if __name__ == '__main':
	Corner(idf_file,Corner)