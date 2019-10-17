import re 
from math import log 
#
# #cd Documents/nlp/ass2/ 
notwordTAG = "UNK"

def getOcuurance(fileName):
    
    testfile = open(fileName, "r") 
    testCurrfile = testfile.readlines()

    count = 0
    words = dict()

    for x in testCurrfile: 
            count += 1
        #if(count < 2): 
            pattern = re.split(r' ', x)
            a =[ re.split(r'/', item)  for item in pattern  if item != '\n' ] 
            for index in range(len(a)):
                #curr= (a[index][0], a[index][1]) 
                word = a[index][0]
                pos = a[index][1]

                
                if word.isalpha:
                    word = word.lower()
                #print("wordddd", word)
                if  word  in words:
                    
                    #innerDict = words.get(curr)
                    if pos in words.get(word): 
                        value = words.get(word).get(pos) 
                        words.get(word).update( {pos: value+1} )
                    
                    else: 
                        words.get(word).update( {pos: 1} )
                else:
                    words.update( {word: {pos: 1}} )
            if(count % 100 == 0):
                print("reading in train file line: ",count)
                #corpus += a
                #print (a)
    returnWords = dict()
    for key,value in words.items():
        item = list(sorted(value, key=value.get, reverse=True))[0]
        #print(key, "sss")
        #print(value)
        returnWords.update({key: item})

    return (returnWords)

def generateFile(fileName, words):
    trainfile = open(fileName, "r") 
    trainfile = trainfile.readlines()

    returnStr= ""
    count = 0
    for x in trainfile: 
            count += 1
        #if(count < 3): 
            
            pattern = re.split(r' ', x)
            for index in range(len(pattern)):
                word = pattern[index]
                if(word == '\n'):
                    returnStr += word
                else:
                    returnStr += findHighestOccurence(word, words)  + " "
                    #print("returnStrreturnStrreturnStr", returnStr )
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
    wordsPOS = getOcuurance(trainfileName)
    #print("wordsPOSwordsPOSwordsPOS", wordsPOS)
    print("zknvzkcxmvnzmcfdnfdsjkfdksjfkjsdfjksjkdfj")
    solution =  generateFile(testfileName, wordsPOS)
    givenSolution = generateStringOfSolution(testSolutionGiven)
    count, total = (getAccuracy(givenSolution,solution))
    
    print("Accuracy is ", count/total* 100)
    
   