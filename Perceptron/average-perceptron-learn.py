import os
import sys
import pickle
import random

fileContents = [] #contains tuples of ("label",{word count} //dictionary of all the words in the email) for all files in train folder
bias = 0
beta = 0
avgWeightsOfWords = {}
spamY = 1
hamY = -1
weightsOfWords = {}
count = 1

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
                            if not avgWeightsOfWords.get(word, False):
                                avgWeightsOfWords[word] = 0
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


def avgPerLearn():
    global bias
    global spamY
    global hamY
    global count
    global beta
    for i in range(30):
        for t in fileContents:
            alpha = 0
            for keys in t[1]:
                alpha += (weightsOfWords[keys] * t[1][keys])
            alpha += bias
            if t[0] == "spam":
                if (spamY * alpha) <= 0:
                    for key in t[1]:
                        weightsOfWords[key] = weightsOfWords[key] + (spamY * t[1][key])
                        avgWeightsOfWords[key] = avgWeightsOfWords[key] + (spamY * count * t[1][key])
                    bias += spamY
                    beta += spamY * count
            elif t[0] == "ham":
                if (hamY * alpha) <= 0:
                    for key in t[1]:
                        weightsOfWords[key] = weightsOfWords[key] + (hamY * t[1][key])
                        avgWeightsOfWords[key] = avgWeightsOfWords[key] + (hamY * count * t[1][key])
                    bias += hamY
                    beta += hamY * count
            count += 1
        random.shuffle(fileContents)
    for key in avgWeightsOfWords:
        avgWeightsOfWords[key] = weightsOfWords[key] - ((1/count) * avgWeightsOfWords[key])
    beta = bias - ((1/count) * beta)
            #print(weightsOfWords)


def dumpData():
    global beta
    global avgWeightsOfWords
    lists = []
    lists.append(avgWeightsOfWords)
    lists.append(beta)
    fp = open("per_model.txt", "wb")
    pickle.dump(lists, fp)
    fp.close()


if __name__ == '__main__':
    if sys.argv.__len__() == 2:
        directoryName = sys.argv[1]
        # print(directoryName)
        # print(type(directoryName))
        parseData(directoryName)
        avgPerLearn()
        dumpData()
    else:
        print("incorrect number of arguments")