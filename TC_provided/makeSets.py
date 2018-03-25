import os
import re

file = raw_input("Please enter the name/path to original training labels file:")
name = raw_input("Please enter name for output (Note: test/train will be appended):")

newTrain = name + "_train.labels"
newTestList = name + "_test.list"
newTestLabels = name + "_test.labels"

trainFile = open(file, 'r')

my_list = []

for counter, line in enumerate(trainFile):
	parts = re.split('[ \n]', line)
	my_list.append([ parts[0], parts[1] ])
	# path = parts[0]
 #    category = parts[1]
trainFile.close()

totalDocs = len(my_list)
numTest = totalDocs/3
numTrain = totalDocs - numTest
print numTrain, numTest

newTrainFile = open(newTrain,'w')
newTestListFile = open(newTestList,'w')
newTestLabelsFile = open(newTestLabels,'w')
 
for counter, element in enumerate(my_list):
	# print counter
 	if (counter+1) > numTrain:
 		print >> newTestListFile, element[0]
 		print >> newTestLabelsFile, element[0], element[1]
 	else:
 		print >> newTrainFile, element[0], element[1]

newTrainFile.close()
newTestLabelsFile.close()
newTestListFile.close()
