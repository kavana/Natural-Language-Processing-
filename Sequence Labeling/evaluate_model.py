import sys
from hw3_corpus_tool import *

fp1 = open(sys.argv[2],'r')
#data = list(get_data(sys.argv[1]))
data = []
for root, dirs, files in os.walk(sys.argv[1], topdown=True):
    for file in files:
        if file.endswith('.csv'):
            fp = open(os.path.join(root, file),"r")
            data.append(get_utterances_from_file(fp))
number = 0
correctlyIdentified = 0
totalTags = 0

def actTag(l):
    at = []
    for i in range(len(l)):
        at.append(l[i].act_tag)
    return at

actTagsTest = []
actTagsUserResult = []
at = []
for i in range(len(data)):
    actTagsTest.append(actTag(data[i]))

for l in fp1.readlines():
    if("Filename" in l):
        if number != 0:
            actTagsUserResult.append(at)
            at  = []
        else:
            number = 1
    else:
        if l != '\n':
            at.append(l.rstrip('\n'))
actTagsUserResult.append(at)

# print(str(len(actTagsUserResult[0])))
# print(len(actTagsTest[0]))
#print(len(actTagsTest))
#print(len(actTagsUserResult))

for i in range(len(actTagsTest)):
    for j in range(len(actTagsTest[i])):
        if actTagsTest[i][j] == actTagsUserResult[i][j]:
            correctlyIdentified += 1
        totalTags += 1

print((correctlyIdentified/totalTags)*100)


#
# print(actTagsTest)
# print(actTagsUserResult)

