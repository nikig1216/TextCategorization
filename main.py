import os
import re
# import nltk
from nltk.tokenize import RegexpTokenizer
# from nltk.tokenize import word_tokenize

class classifier:
    def __init__(self):
        self.totalTrainingDocs = 0
        self.categories = {}
    def assignPriors(self):
        for c in self.categories:
            c.assignPrior(self.totalTrainingDocs)
    def assignAllCondProbs(self):
        for c in self.categories:
            c.assignCondProbs()

    class category:
        def __init__(self,name,plusOne):
            self.catName = name
            self.count = 0+plusOne
            self.vector = {}
            self.wordsSeen = 0

        def assignPrior(self,totalNumberOfTrainingDocs):
            self.prior = self.count/totalNumberOfTrainingDocs
        def vectorize(self,wordsInDoc):
            for t in wordsInDoc:
                self.wordsSeen += 1
                if t in self.vector:
                    self.vector[t].count += 1
                else:
                    self.vector[t] = classifier.category.word()
        def assignCondProbs(self):
            for t in self.vector:
                t.assignCondProb(self.vector.__len__(),self.wordsSeen)

        class word:
            smoothingParam = .1

            def __init__(self):
                self.count = 1
                self.condProb = None

            def assignCondProb(self,totalWordsInVocabulary,totalWordsSeen):
                self.condProb = (self.count + self.smoothingParam)/(totalWordsSeen+(self.smoothingParam*totalWordsInVocabulary))


my_classifier = classifier()

print('Welcome to my text categorization program!')
devmode = raw_input('Enter 1 for devmode: ')
if devmode == '1':
    trainFileList = "/Users/NicholasGao/CLionProjects/TextCategorizer/cmake-build-debug/TC_provided/corpus1_train.labels"
    testFileList = "/Users/NicholasGao/CLionProjects/TextCategorizer/cmake-build-debug/TC_provided/corpus1_test.list"
    outFile = "out.txt"
else:
    trainFileList = raw_input('Please enter the (name and path to the) list of training documents: ')
    testFileList = raw_input('Please enter the (path to the) list of test documents: ')
    outFile = raw_input('Please enter the desired output file name: ')
# print trainFileList

regexptoken = RegexpTokenizer(r'\w+')
file = open(trainFileList,'r')
for counter,line in enumerate(file):
    # print line
    parts = re.split('[ \n]',line)
    path = parts[0]
    category = parts[1]
    docFilePath = os.path.join(trainFileList.rsplit('/', 1)[0], path.split('/', 1)[1])
    # print docFilePath
    docFile = open(docFilePath, 'r')

    my_classifier.totalTrainingDocs += 1
    # print docFile.read().lower()
    # print word_tokenize(docFile.read().lower())
    docWords = regexptoken.tokenize(docFile.read().lower())
    # print docWords

    if category in my_classifier.categories: # Has This Class Been Seen Before?
        my_classifier.categories[category].count +=1
        # Fill in vector
        my_classifier.categories[category].vectorize(docWords)
    else:
        cat = my_classifier.category(category,1)
        my_classifier.categories[category] = cat
        # Fill the vector in
        my_classifier.categories[category].vectorize(docWords)

    docFile.close()
    # if counter == 0:
    #     break

# print my_classifier.categories['Cri'].catName

file.close()