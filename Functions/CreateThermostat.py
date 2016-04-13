from pint import UnitRegistry
from eppy import modeleditor
from eppy.modeleditor import IDF

# Context: Design assistance projects.
# Function: Create constant thermostat setpoint.
# Important Notes:
#				- The thermostat is created using the HVACTemplate hence is only compatible with template systems.
# Arg. Values: 
#				- HtgSetpoint: Any > 0.
#				- ClgSetpoint: Any > 0.

def CreateThermostat(idf_file,*args):
	# Define the Unit Registery used for unit conversion
	ureg = UnitRegistry()

	# Object and variables initialization
	HtgSP = args[0][0]
	ClgSP = args[0][1]
	
	# Conversion of the SP from IP to SI
	HtgSP = float(HtgSP)
	Htg = ureg.Quantity
	HtgSPIP = Htg(float(HtgSP), ureg.degF)
	HtgSPSI = HtgSPIP.to('degC')
	ClgSP = float(ClgSP)
	Clg = ureg.Quantity
	ClgSPIP = Clg(float(ClgSP), ureg.degF)
	ClgSPSI = ClgSPIP.to('degC')
	
	# Create the thermostat
	Thermostat = idf_file.newidfobject("HVACTEMPLATE:THERMOSTAT")
	Thermostat.Name = "Thermostat-Htg"+str(int(HtgSP))+"F-Clg"+str(int(ClgSP))+"F"
	Thermostat.Constant_Heating_Setpoint = HtgSPSI.magnitude
	Thermostat.Constant_Cooling_Setpoint = ClgSPSI.magnitude
	
if __name__ == '__main':
	CreateThermostat(idf_file,*args)