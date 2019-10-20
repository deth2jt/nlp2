import re 
from math import log 
import string

#
# #cd Documents/nlp/ass2/ 
notwordTAG = "UNK"
startTAG = '<s>'
endTAG = '</s>'

def getHMM(fileName):
    
    testfile = open(fileName, "r") 
    testCurrfile = testfile.readlines()

    count = 0
    transistionDict = dict()
    emissionDict = dict()
    tagUnigram = dict()

    for x in testCurrfile: 
            count += 1
        #if(count < 5): 
            #x = x.translate(str.maketrans('', '', string.punctuation))
            #print("ss",x)
            #x = re.sub('[.;!,?"-`]', '',x)
            pattern = re.split(r' ', x)
            a =[ re.split(r'/', item)  for item in pattern  if item != '\n' ] 
            #print(a)

           

            prevWord = ""
            prevTag = ""

            for index in range(len(a)):
                #curr= (a[index][0], a[index][1]) 
                word = a[index][0]
                pos = a[index][1]
                word = word.replace('\n', '')

                
                if word.isalpha:
                    word = word.lower()
                #word = word.replace('\n', '')
                #print("wordddd", word)

                if index == 0:
                    prevWord = '<s>'
                    prevTag = '<s>'

                emission = (pos, word)
                transistion = (prevTag, pos)

                
                (transistionDict,emissionDict, tagUnigram) = updateDicts(transistionDict,emissionDict, tagUnigram, emission, transistion)

                prevWord = word
                prevTag = pos

            if(count % 100 == 0):
                print("reading in train file line: ",count)
                #corpus += a
                #print (a)
            word = '</s>'
            pos = '</s>'

            emission = (pos, word)
            transistion = (prevTag, pos)


            (transistionDict,emissionDict, tagUnigram) = updateDicts(transistionDict,emissionDict, tagUnigram, emission, transistion)
            if  pos  in tagUnigram: 
                count = tagUnigram.get(pos)
                tagUnigram.update( {pos: count+1} )
            else:
                tagUnigram.update(  {pos: 1} )
            
    return (transistionDict,emissionDict, tagUnigram)

def updateDicts(transistionDict,emissionDict, tagUnigram, emission, transistion):
    prevTag = transistion[0]
    if  prevTag  in tagUnigram: 
        count = tagUnigram.get(prevTag)
        tagUnigram.update( {prevTag: count+1} )
    else:
        tagUnigram.update(  {prevTag: 1} )
    
    if  emission  in emissionDict:
        count = emissionDict.get(emission)
        emissionDict.update( {emission: count+1}  )
    else:
        emissionDict.update( {emission: 1} )
    if  transistion  in transistionDict:
        count = transistionDict.get(transistion) 
        transistionDict.update( {transistion: count+1}  )
    else:
        transistionDict.update( {transistion: 1} )
    return (transistionDict,emissionDict, tagUnigram)
            
def generateFile(fileName, transistionDict,emissionDict, tagUnigram):
    trainfile = open(fileName, "r") 
    trainfile = trainfile.readlines()

    returnDict = dict()
    count = 0
    for x in trainfile: 
        count += 1
        if(count < 2): 
            
            pattern = re.split(r' ', x)
            

            print("len(tagUnigram)",pattern)
            wordCount = 0
            for index in range(len(pattern)):
                word = pattern[index]
                
                #print("countcountcountcount", count)
                emisstransDict = getEmissionTransProb(word, wordCount, transistionDict,emissionDict, tagUnigram) 
                print("wordwordword", word)
                returnDict.update({word: emisstransDict}) 
                #print("returnDictreturnDictreturnDict", returnDict )
                #print("transistionDicttransistionDicttransistionDict", transistionDict )

                if('\n' in word):
                    #getViterbiPath(returnDict)
                    emisstransDict = getEmissionTransProb(word, -1, transistionDict,emissionDict, tagUnigram) 
                    
                    #print(returnDict)
                #print("emisstransDictemisstransDictemisstransDict", emisstransDict)
                    
                wordCount= wordCount +1

            viterbiMax = 0
            viterbiDict = dict()
            viterbiCount = 0
            for key,value in returnDict.items():
                
                #viterbiMax = highest[1]
                #highest = 0
                viterbiDictInner = dict()

                viterbiMax = sorted(value.items(), reverse=True, key=lambda x: x[1])[0][1]

                for key1,value1 in value.items():
                    #print("value1value1value1", value1)
                    if(viterbiCount > 0):
                        viterbiDictInner.update( {key1: value1*viterbiMax}  )
                    else:
                        viterbiDictInner.update( {key1: value1}  )
                    viterbiCount = viterbiCount +1

                viterbiDict.update( {key: viterbiDictInner}  )
                    
            for key,value in viterbiDict.items():
                
                #viterbiMax = highest[1]
                #highest = 0
                #viterbiDictInner = dict()

                maxIT = sorted(value.items(), reverse=True, key=lambda x: x[1])[0]
                maxIT2 = sorted(value.items(), reverse=True, key=lambda x: x[1])[1]
                print("viterbi", maxIT)
                

            for key,value in viterbiDict.items():
                
                #viterbiMax = highest[1]
                #highest = 0
                #viterbiDictInner = dict()

                maxIT = sorted(value.items(), reverse=True, key=lambda x: x[1])[0]
                maxIT2 = sorted(value.items(), reverse=True, key=lambda x: x[1])[1]
                
                print("beam search", maxIT, maxIT2)


            if(count % 10 == 0):
                print("reruyrneddddddd")
                print("reading in test file line: ",count)
    #return returnStr

def foo(count, length):
    if count == length:
        return -1
    elif count > 0:
        return 1
    return count 


def getEmissionTransProb(word, count, transistionDict,emissionDict, tagUnigram):

    toLower = word.isalpha()
    wordDict = dict()
    print("counttttttttt", count)
    if count == 0:
        print("0000000000")
        timinusone = startTAG

        for key2, value2 in tagUnigram.items():
            ti = key2
            if toLower:
                emission = (ti, word.lower())
            else:
                emission = (ti, word)
            transistion = (timinusone, ti)


            emissionProb = addOneSmoothing(emission, emissionDict, tagUnigram)
            transistionProb = addOneSmoothing(transistion, transistionDict, tagUnigram)

            emissiontransPRob = emissionProb * transistionProb
            wordDict.update(  {(timinusone,ti) : emissiontransPRob} )
            if(transistion == ('<s>', 'in')):
                print("emissionProb, transistionProb", emissionProb, transistionProb)
    elif (count == -1):
        print("-------1111111111")
        for key, value1 in tagUnigram.items():
            timinusone = key

            
            ti = '</s>'
            if toLower:
                emission = (ti, word.lower())
            else:
                emission = (ti, word)
            transistion = (timinusone, ti)
            emissionProb = addOneSmoothing(emission, emissionDict, tagUnigram)
            transistionProb = addOneSmoothing(transistion, transistionDict, tagUnigram)

            emissiontransPRob = emissionProb * transistionProb
            wordDict.update(  {(timinusone,ti) : emissiontransPRob} )
    else:
        print("elselseslesle")
        for key, value1 in tagUnigram.items():
            timinusone = key

            for key2, value2 in tagUnigram.items():
                ti = key2
                if toLower:
                    emission = (ti, word.lower())
                else:
                    emission = (ti, word)
                transistion = (timinusone, ti)
                emissionProb = addOneSmoothing(emission, emissionDict, tagUnigram)
                transistionProb = addOneSmoothing(transistion, transistionDict, tagUnigram)

                emissiontransPRob = emissionProb * transistionProb
                wordDict.update(  {(timinusone,ti) : emissiontransPRob} )
                
                    
    
    return wordDict

    
       
def addOneSmoothing(probPair ,transistionDict, tagUnigram):
    #emission = emissionDict.get((t1, word))
    emissiontransistion = transistionDict.get(probPair)
    unigram = tagUnigram.get(probPair[0])
    #print("probPair[0]", probPair[0])
    if emissiontransistion is None:
        emissiontransistion = 0
    addOneProb = float(emissiontransistion + 1) / float(unigram + len(tagUnigram))
    #print("emissiontransistion, unigram, len(tagUnigram)", emissiontransistion, unigram, len(tagUnigram))
    return addOneProb


def generateStringOfSolution(fileName):
    file = open(fileName, "r") 
    file = file.readlines()

    returnStr= ""
    count = 0

    for x in file: 
            count += 1
        #if(count < 3): 
            

            pattern = re.split(r' ', x)
            for index in range(len(pattern)):
                word = pattern[index]
                if(word == '\n'):
                    returnStr += word
                else:
                    returnStr += (word + " ")
    return (returnStr)

def getAccuracy(testSolutionGiven, solution):
    
    givenSOlution = testSolutionGiven.split(' ')
    mySOlution = solution.split(' ')
    
    print(givenSOlution[0:5])
    print(mySOlution[0:5])

    lenhthy = len(givenSOlution)
    count = 0
    for index in range(lenhthy): 
        if(givenSOlution[index] == mySOlution[index]):
            count+=1
    return (count, lenhthy)

    

if __name__ == '__main__': 
    trainfileName = "brown.train.tagged.txt" 
    testfileName = "brown.test.txt" 
    testSolutionGiven = "brown.test.tagged.txt"
    transistionDict,emissionDict, tagUnigram = getHMM(trainfileName)

    #print("wordsPOSwordsPOSwordsPOS", tagUnigram)

    print("zknvzkcxmvnzmcfdnfdsjkfdksjfkjsdfjksjkdfj")
    generateFile(testfileName, transistionDict,emissionDict, tagUnigram)

    '''
    givenSolution = generateStringOfSolution(testSolutionGiven)
    count, total = (getAccuracy(givenSolution,solution))
    
    print("Accuracy is ", count/total* 100)

    '''
    
   