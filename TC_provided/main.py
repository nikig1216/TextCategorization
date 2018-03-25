# Nicholas Gao
# ECE467 Natural Language Processing
# Professor Sable
# Spring 2018
# Project 1: Text Categorization

"""This program represents my implementation of a text categorizer that uses Naive Bayes to make its decisions."""

import os
import math
import re
# import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# stopwords = nltk.download('stopwords')


class Classifier:

    smoothingParam = .1

    def __init__(self):
        self.totalTrainingDocs = 0
        self.categories = {}

    def assignPriors(self):
        for c in self.categories:
            self.categories[c].assignPrior(self.totalTrainingDocs)

    def assignAllCondProbs(self):
        for c in self.categories:
            # print c
            self.categories[c].assignCondProbs(self.smoothingParam)

    def makeArgMaxDict(self):
        amDict = {}
        for c in self.categories:
            # print c
            amDict[c] = None
        # print amDict
        return amDict

    class Category:

        def __init__(self, name, plus_one):
            self.catName = name
            self.count = 0.0 + plus_one
            self.vector = {}
            self.wordsSeen = 0
            self.unkCondProb = None

        def assignPrior(self,totalNumberOfTrainingDocs):
            self.prior = math.log(self.count/totalNumberOfTrainingDocs)

        def vectorize(self, wordsInDoc):
            for t in wordsInDoc:
                self.wordsSeen += 1
                if t in self.vector:
                    self.vector[t].count += 1
                else:
                    self.vector[t] = Classifier.Category.Word()

        def assignCondProbs(self, smoothingParam):
            for t in self.vector:
                self.vector[t].assignCondProb(self.vector.__len__(), self.wordsSeen, smoothingParam)
            self.unkCondProb = math.log(smoothingParam/(self.wordsSeen+(smoothingParam*self.vector.__len__())))

        class Word:

            def __init__(self):
                self.count = 1
                self.condProb = None

            def assignCondProb(self, totalWordsInVocabulary, totalWordsSeen, smoothingParam):
                self.condProb = math.log((self.count + smoothingParam)/(totalWordsSeen+(smoothingParam*totalWordsInVocabulary)))


my_classifier = Classifier()

print('Welcome to my text categorization program!')
# devmode = raw_input('Enter 1 for devmode: ')

trainFileList = raw_input('Please enter the (name and path to the) list of training documents: ')
if trainFileList == "itsnicholas":
    trainFileList = "/Users/NicholasGao/CLionProjects/TextCategorizer/cmake-build-debug/TC_provided/corpus1_train.labels"
    testFileList = "/Users/NicholasGao/CLionProjects/TextCategorizer/cmake-build-debug/TC_provided/corpus1_test.list"
    outFile = "tc_out.txt"
else:
    testFileList = raw_input('Please enter the (path to the) list of test documents: ')
    outFile = raw_input('Please enter the desired output file name: ')
# print trainFileList

regexptoken = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

## Begin Training
trainFile = open(trainFileList, 'r')
for counter, line in enumerate(trainFile):
    # print line
    parts = re.split('[ \n]', line)
    path = parts[0]
    category = parts[1]
    trainFileList_pieces = trainFileList.rsplit('/', 1)  # Splits training labels file into parent dir and file
    # print trainFileList_pieces
    pardir = ""
    if len(trainFileList_pieces) == 2:  # Addresses the case where parent dir not given in training label path
        pardir = trainFileList_pieces[0]
        # print pardir
    docFilePath = os.path.join(pardir, path.split('/', 1)[1])
    # print docFilePath
    docFile = open(docFilePath, 'r')
    # stall = raw_input("pause:")
    my_classifier.totalTrainingDocs += 1
    # print docFile.read().lower()
    # print word_tokenize(docFile.read().lower())
    # docWords = regexptoken.tokenize(docFile.read().lower())
    docWords = word_tokenize(docFile.read().lower())
    # docWords = word_tokenize(docFile.read())
    # print docWords

    # filterDocWords = []
    # for r in docWords:
    #     if not r in stop_words:
    #         filterDocWords.append(r)
    # print filterDocWords
    # docWords = filterDocWords

    if category in my_classifier.categories:  # Has This Class Been Seen Before?
        my_classifier.categories[category].count += 1
        # Fill in vector
        my_classifier.categories[category].vectorize(docWords)
    else:
        cat = my_classifier.Category(category, 1)
        my_classifier.categories[category] = cat
        # Fill the vector in
        my_classifier.categories[category].vectorize(docWords)

    docFile.close()
    # if counter == 0:
    #     break
# End Loop Over Training Docs
my_classifier.assignPriors()
my_classifier.assignAllCondProbs()

# print my_classifier.categories['Cri'].catName

trainFile.close()

## BEGIN Testing/Classification
testFile = open(testFileList, 'r')
output = open(outFile, 'w')
amDict = my_classifier.makeArgMaxDict()

for counter, line in enumerate(testFile):
    # print line
    parts = re.split('[ \n]', line)  # Shaves off newline, during training it would've separated the label too.
    path = parts[0]
    # print parts
    testFile_pieces = testFileList.rsplit('/', 1)
    pardir = ""
    if len(testFile_pieces) == 2:
        pardir = testFile_pieces[0]
    docFilePath = os.path.join(pardir, path.split('/', 1)[1])
    # print docFilePath
    testDocFile = open(docFilePath, 'r')

    # testDocWords = regexptoken.tokenize(testDocFile.read().lower())
    testDocWords = word_tokenize(testDocFile.read().lower())
    # testDocWords = word_tokenize(testDocFile.read())
    # print testDocWords
    # filterTestDocWords = []
    # for r in testDocWords:
    #     if not r in stop_words:
    #         filterTestDocWords.append(r)
    # testDocWords = filterTestDocWords

    for c in my_classifier.categories:
        score = my_classifier.categories[c].prior

        for t in testDocWords:
            if t in my_classifier.categories[c].vector:
                score += my_classifier.categories[c].vector[t].condProb
            else:
                score += my_classifier.categories[c].unkCondProb
        amDict[c] = score

    # Iterate Over ArgMaxList to find Max
    # print amDict
    decision = max(amDict.iterkeys(), key=(lambda key: amDict[key]))
    # print decision
    # output.write(path,decision)
    print >> output, path, decision  # Write to file

    testDocFile.close()
    # if counter == 0:
    #     break
testFile.close()
output.close()
