import os
import sys
import pickle
import random

fileContents = [] #contains tuples of ("label",{word count} //dictionary of all the words in the email) for all files in train folder
bias = 0
spamY = 1
hamY = -1
weightsOfWords = {}

def parseData(nameOfDir):
    global bias
    for root, dirs, files in os.walk(nameOfDir, topdown=True):
        if os.path.basename(root) == 'ham' or os.path.basename(root) == 'spam':
            for file in files:
                if file.endswith('.txt'):
                    fp = open(os.path.join(root, file), "r", encoding="latin1")
                    countOfWords = {}
                    for sentence in fp:
                        sentence = sentence.rstrip('\n').strip(" ")
                        words = sentence.split(" ")
                        for word in words:
                            if not weightsOfWords.get(word, False):
                                weightsOfWords[word] = 0
                            if not countOfWords.get(word, False):
                                countOfWords[word] = 1
                            else:
                                countOfWords[word] += 1
                    if os.path.basename(root) == 'ham':
                        fileContents.append(("ham", countOfWords))
                        fp.close()
                    elif os.path.basename(root) == 'spam':
                        fileContents.append(("spam", countOfWords))
                    fp.close()


def perLearn():
    global bias
    global spamY
    global hamY
    for i in range(20):
        for t in fileContents:
            alpha = 0
            for keys in t[1]:
                alpha += (weightsOfWords[keys] * t[1][keys])
            alpha += bias
            if t[0] == "spam":
                if (spamY * alpha) <= 0:
                    for key in t[1]:
                        weightsOfWords[key] = weightsOfWords[key] + (spamY * t[1][key])
                    bias += spamY
            elif t[0] == "ham":
                if (hamY * alpha) <= 0:
                    for key in t[1]:
                        weightsOfWords[key] = weightsOfWords[key] + (hamY * t[1][key])
                    bias += hamY
        random.shuffle(fileContents)
    #print(weightsOfWords)


def dumpData():
    global bias
    global weightsOfWords
    lists = []
    lists.append(weightsOfWords)
    lists.append(bias)
    fp = open("per_model.txt", "wb")
    pickle.dump(lists, fp)
    fp.close()


if __name__ == '__main__':
    if sys.argv.__len__() == 2:
        directoryName = sys.argv[1]
        # print(directoryName)
        # print(type(directoryName))
        parseData(directoryName)
        perLearn()
        dumpData()
    else:
        print("incorrect number of arguments")