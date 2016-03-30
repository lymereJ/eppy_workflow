from eppy import modeleditor
from eppy.modeleditor import IDF
import csv
import importdir

importdir.do("FunctionsLibrary",globals())
IDDFile = 'C:\EnergyPlusV8-3-0\Energy+.idd'
IDF.setiddname(IDDFile)

BatchProcesingFile = open("BatchProcessing.csv","r")
BatchProcessing = list(csv.reader(BatchProcesingFile, delimiter=',', quotechar=chr(34)))
Idx = 0

for i in range(0,len(BatchProcessing)):
	print str(Idx)+" out of "+str(len(BatchProcessing))
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
	Idx = Idx + 1

print "Done."