from eppy import modeleditor
from eppy.modeleditor import IDF

import csv
import TimeStep
import Orientation
import LPD
import EPD
import PeopleNumber
import WindowSHGC
import WindowUValue
import WWR
import VentilationFlow
import FanEff
import Length
import Width
import Roof
import Corner
import EffectiveLeakageArea
import VentingTemp
import VentingMethod
import WallUValue
import RoofUValue
import WindowInfiltration
import Cooling
import VentingFactor
import InternalMass

IDDFile = 'C:\EnergyPlusV8-3-0\Energy+.idd'
IDF.setiddname(IDDFile)

BatchProcesingFile = open("BatchProcessing.csv","r")
BatchProcessing = list(csv.reader(BatchProcesingFile, delimiter=',', quotechar=chr(34)))
Counter = 0

for i in range(0,len(BatchProcessing)):
	print str(Counter)+" out of "+str(len(BatchProcessing))
	row = BatchProcessing[i]
	nbcol = len(row)
	if row[0] <> 'idf' and row[0] <> '-':
		idf_file = IDF(row[0])
		NewNameArguments = ""
		for j in range(2,nbcol):
			item = BatchProcessing[0][j]
			func = getattr(eval(item),item)
			arguments = row[j]
			NewNameArguments = NewNameArguments + "-" + arguments
			func(idf_file, arguments)
		idf_file.saveas(row[1][:-4]+".idf")
	Counter = Counter + 1

print "Done."