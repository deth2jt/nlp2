import re 
from math import log 
#
# #cd Documents/nlp/ass2/ 
notwordTAG = "UNK"

def getHMM(fileName):
    
    testfile = open(fileName, "r") 
    testCurrfile = testfile.readlines()

    count = 0
    transistionDict = dict()
    emissionDict = dict()
    tagUnigram = dict()

    for x in testCurrfile: 
        count += 1
        if(count < 15): 
            pattern = re.split(r' ', x)
            a =[ re.split(r'/', item)  for item in pattern  if item != '\n' ] 
            #print(a)

           

            prevWord = ""
            prevTag = ""

            for index in range(len(a)):
                #curr= (a[index][0], a[index][1]) 
                word = a[index][0]
                pos = a[index][1]

                
                if word.isalpha:
                    word = word.lower()
                #print("wordddd", word)

                if index == 0:
                    prevWord = '<s>'
                    prevTag = '<s>'

                emission = (prevWord, word)
                transistion = (prevTag, pos)

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


                prevWord = word
                prevTag = pos

            if(count % 100 == 0):
                print("reading in train file line: ",count)
                #corpus += a
                #print (a)
            

            if  prevTag  in tagUnigram:
                count = tagUnigram.get(prevTag)
                tagUnigram.update( {prevTag: count+1}  )
            else:
                tagUnigram.update(  {prevTag: 1} )

    return (transistionDict,emissionDict, tagUnigram)

def generateFile(fileName, transistionDict,emissionDict, tagUnigram):
    trainfile = open(fileName, "r") 
    trainfile = trainfile.readlines()

    returnStr= ""
    count = 0
    for x in trainfile: 
            count += 1
        #if(count < 3): 
            
            pattern = re.split(r' ', x)
            prevWord = '<s>'
            prevTag = '<s>'
            print("len(tagUnigram)",tagUnigram)
            for index in range(len(pattern)):
                word = pattern[index]
                if(word == '\n'):
                    returnStr += word
                else:
                    returnStr += findHighestOccurence(word, words)  + " "
                    #print("returnStrreturnStrreturnStr", returnStr )
                prevWord = '<s>'
                prevTag = '<s>'
            if(count % 10 == 0):
                print("reading in test file line: ",count)
    return returnStr

def findHighestOccurence(word, listOfWordPOS):

    toLower = word.isalpha()
    if(word.isalpha()):
        if word.lower() in listOfWordPOS:
            #print("worsssasasdasdasdasdasd" , word, listOfWordPOS.get(word.lower()))
            return (word + "/" + listOfWordPOS.get(word.lower()))
        else:
            return (word + "/"+ notwordTAG)
    else:
        if word in listOfWordPOS:
            return (word + "/" + listOfWordPOS.get(word.lower()))
        else:
            return (word + "/"+ notwordTAG)
       
        
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

    #print("wordsPOSwordsPOSwordsPOS", wordsPOS)

    print("zknvzkcxmvnzmcfdnfdsjkfdksjfkjsdfjksjkdfj")
    solution =  generateFile(testfileName, transistionDict,emissionDict, tagUnigram)

    '''
    givenSolution = generateStringOfSolution(testSolutionGiven)
    count, total = (getAccuracy(givenSolution,solution))
    
    print("Accuracy is ", count/total* 100)

    '''
    
   