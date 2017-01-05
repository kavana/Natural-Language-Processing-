from hw3_corpus_tool import *
import pycrfsuite
import sys


if sys.argv.__len__() != 4:
    print("Incorrect number of arguments")
    exit()

a = list(get_data(sys.argv[1]))


def features(l):
    feature = []
    for j in range(len(l)):
        sentence = []
        if j == 0:
            featureDU = ['changeSpeaker:True']
            prevSpeaker = l[j]
        elif l[j].speaker != prevSpeaker:
            featureDU = ['changeSpeaker:True']
            prevSpeaker = l[j]
        else:
            # featureDU = ['changeSpeaker:False']
            prevSpeaker = l[j]
        if j == 0:
            featureDU.extend(['firstUtterance:True'])
        # else:
        #     featureDU.extend(['firstUtterance:False'])
        if l[j].pos != None:
            for x in range(len(l[j].pos)):
               # if not(l[j].pos[x].token in stopWords):
                featureDU.extend(['TOKEN_' + (l[j].pos[x].token).lower()])
                featureDU.extend(['POS_' + l[j].pos[x].pos])
                sentence.append((l[j].pos[x].token).lower())
            word = ""
            for y in range(len(sentence)):
                if (len(word.split(" ")) == 1 and word != ""):
                    word = word + " " + sentence[y]
                    featureDU.extend(['Bigrams_' + word])
                    word = ""
                word = word + sentence[y]
                # if y%2 == 0:
                #     word = ""
                #     word = word + l[j].pos[y].token
                # else:
                #     word  = word +" "+ l[j].pos[y].token
                #     featureDU.extend(['Bigrams_' + word])
            if len(sentence) == 1:
                featureDU.extend(['Bigrams_' + word])
        if '?' in l[j].text:
            featureDU.extend(['question:True'])
        if '!' in l[j].text:
            featureDU.extend(['exclamation:True'])
        feature.append(featureDU)
    return feature


def actTag(l):
    at = []
    for i in range(len(l)):
        at.append(l[i].act_tag)
    return at


f = []
actTags = []
for i in range(len(a)):
    f.append(features(a[i]))
    actTags.append(actTag(a[i]))

# print(f)
# print(actTags)
trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(f, actTags):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,  # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 100,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})
trainer.train('advanced.crfsuite')
tagger = pycrfsuite.Tagger()
tagger.open('advanced.crfsuite')
f_test = []
devfiles = []
for root, dirs, files in os.walk(sys.argv[2], topdown=True):
    dev = []
    for file in files:
        if file.endswith('.csv'):
            fp = open(os.path.join(root, file),"r")
            devfiles.append(file)
            dev.append(get_utterances_from_file(fp))


for m in range(len(dev)):
    f_test.append(features(dev[m]))

y_pred = [tagger.tag(xseq) for xseq in f_test]
#print(y_pred)
#print(devfiles)

ofp = open(sys.argv[3], "w")
for i in range(len(y_pred)):
    ofp.write('Filename="' + devfiles[i] + '"\n')
    for j in y_pred[i]:
        ofp.write(j + '\n')
    ofp.write('\n')

