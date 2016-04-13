from eppy import modeleditor
from eppy.modeleditor import IDF
import csv
import importdir

# Initialization #1
importdir.do("Functions",globals())
IDDFile = 'C:\EnergyPlusV8-3-0\Energy+.idd'
IDF.setiddname(IDDFile)
BatchProcesingFile = open("BatchProcessing.csv","r")
BatchProcessing = list(csv.reader(BatchProcesingFile, delimiter=',', quotechar=chr(34)))
Idx = 0

for i in range(0,len(BatchProcessing)):
	# Display the progress of the script
	if Idx >= 2:
		print "Creating "+str(Idx-1)+" out of "+str(len(BatchProcessing)-2)+" models."
	
	# Initialization #2
	NbRows = BatchProcessing[i]
	if NbRows[0] <> 'idf' and NbRows[0] <> '-':
		# Initialization #3
		idf_file = IDF(NbRows[0])
		
		# Iterates throught the CSV file and execute the specified functions
		for j in range(2,len(NbRows)):
		
			# Retrieve the user input arguments
			arguments = NbRows[j].split(",")
			
			#print str(len(arguments))+" " +str(arguments[0])
			# If not argument is specified do not execute the function
			if not(len(arguments) == 1 and arguments[0] == "-"):
				item = BatchProcessing[0][j]
				func = getattr(eval(item),item)
				func(idf_file, arguments)
		
		# Save the modified IDF file		
		idf_file.saveas(NbRows[1][:-4]+".idf")
	Idx = Idx + 1

print "Done."