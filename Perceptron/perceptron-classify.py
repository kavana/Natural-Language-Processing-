import pickle
import sys
import os
import math

weightsOfWords = {}
bias = 0
result = ""
devSpamFileCount = 0
devHamFileCount = 0
predictedSpamFileCount = 0
predictedHamFileCount = 0
correctlyClassifiedSpamFileCount = 0
correctlyClassifiedHamFileCount = 0

def extractData():
    global weightsOfWords
    global bias
    myData = pickle.load(open("per_model.txt", "rb"))
    weightsOfWords = myData[0]
    bias = myData[1]


def per_classify(nameOfDir,outputFile):
    global devHamFileCount
    global devSpamFileCount
    global predictedSpamFileCount
    global predictedHamFileCount
    global correctlyClassifiedHamFileCount
    global correctlyClassifiedSpamFileCount
    global result
    for root, dirs, files in os.walk(nameOfDir, topdown=True):
        for file in files:
            if file.endswith('.txt'):
                alpha = 0
                fp = open(os.path.join(root, file), "r", encoding="latin1")
                for sentence in fp:
                    sentence = sentence.rstrip('\n')
                    words = sentence.split(" ")
                    for word in words:
                        if weightsOfWords.get(word,False):
                            alpha += weightsOfWords[word]
                alpha += bias
                if (alpha > 0):
                    result = result + "spam " + os.path.join(root, file) + "\n"
                    predictedSpamFileCount += 1
                    if os.path.basename(root) == "spam":
                        correctlyClassifiedSpamFileCount += 1
                else:
                    result = result + "ham " + os.path.join(root, file) + "\n"
                    predictedHamFileCount += 1
                    if os.path.basename(root) == "ham":
                        correctlyClassifiedHamFileCount += 1
                if os.path.basename(root) == "ham":
                    devHamFileCount += 1
                if os.path.basename(root) == "spam":
                    devSpamFileCount += 1
                fp.close()
    fp1 = open(outputFile, "w")
    fp1.write(result)
    fp1.close()


def evaluateResult():
    global devHamFileCount
    global devSpamFileCount
    global predictedSpamFileCount
    global predictedHamFileCount
    global correctlyClassifiedHamFileCount
    global correctlyClassifiedSpamFileCount
    print("Performance on the development data with 100% of the training data with enhancement")
    if devSpamFileCount != 0:
        if predictedSpamFileCount != 0:
            spamPrecision = round(correctlyClassifiedSpamFileCount / predictedSpamFileCount, 2)
            spamRecall = round(correctlyClassifiedSpamFileCount / devSpamFileCount, 2)
            spamF1Score = round((2 * spamPrecision * spamRecall) / (spamPrecision + spamRecall), 2)
            print("spam Precision: ", spamPrecision)
            print("spam Recall: ", spamRecall)
            print("spam F1 Score: ", spamF1Score)
        else:
            print("predicted spam file count is zero")
    else:
        print("given spam file count is 0")
    if devHamFileCount != 0:
        if predictedHamFileCount != 0:
            hamPrecision = round(correctlyClassifiedHamFileCount / predictedHamFileCount, 2)
            hamRecall = round(correctlyClassifiedHamFileCount / devHamFileCount, 2)
            hamF1Score = round((2 * hamPrecision * hamRecall) / (hamPrecision + hamRecall), 2)
            print("ham Precision: ", hamPrecision)
            print("ham Recall: ", hamRecall)
            print("ham F1 Score: ", hamF1Score)
        else:
            print("predicted ham file count is zero")
    else:
        print("given ham file count is 0")


if __name__ == "__main__":
    if sys.argv.__len__() == 3:
        directoryName = sys.argv[1]
        outputFileName = sys.argv[2]
        extractData()
        per_classify(directoryName,outputFileName)
        evaluateResult()

    else:
        print("invalid number of arguments")
