import pickle
import random


def wordFrequencies(theFile):
    text_file = open (theFile, "r")
    successors = {}
    previous = 'the'
    for line in text_file:
        words = line.split()
        for word in words:
            word = word.lower()
            if previous in successors:
                entry = successors[previous]
                if word in entry :
                    entry[word] += 1
                else :
                    entry[word] = 1
            else:
                successors[previous] = {word:1}
            previous = word
    return successors


def generateProbabilityList(theDict) : 
	result = []
	theList = theDict.keys()
	for i in theList : 
		for j in range(0, theDict.get(i)) : 
			result = result + [i]
	print result
	return result

f = open("pickled_word_to_syllables.txt","rb")
syllablesDict = pickle.load(f)

def checkSyllables(theWord, lineSyllables, maxSyllables) : 
	syllableCount = 0
	try :
		syllableCount = syllablesDict.get(theWord)
	except Exception as e:
		print(e)
		return 0
	if (syllableCount is None) or (int(syllableCount) + lineSyllables > maxSyllables): 
		return 0
	else : 
		return syllableCount


def getLine(theWord, theDict, totalSyllables) :
	line = ""
	syllables = 0
	while(syllables < totalSyllables) : 

		nextWordDict = theDict.get(theWord)
		probabilityList = generateProbabilityList(nextWordDict)
		theWord = random.choice(probabilityList).lower()
		numSyllables = checkSyllables(theWord, syllables, totalSyllables)
		while (numSyllables == 0 and len(probabilityList) != 0) : 
			theWord = random.choice(probabilityList).lower()
			probabilityList.remove(theWord)
			numSyllables = checkSyllables(theWord, syllables, totalSyllables)

		if(len(probabilityList) == 0) : 
			return False
		line += theWord + " "
		syllables += int(numSyllables)
	return line[0].upper() + line[1:-1]


def writeLine(theWord, theDict, numSyllables) : 
	line = getLine(theWord,theDict,numSyllables)
	if line == False : 
		while(line == False) : 
			line = getLine(theWord,theDict,numSyllables)
		return line
	else : 
		return line


def writeHaiku() : 
	print "Whose style of writing would you like to emulate?"
	print "Give the name of a text file that contains their writing."
	print "If you'd like to use the default file, just press enter."
	goOn = False
	while(goOn == False) :
		theFile = raw_input()
		if theFile == "" : 
			print "Using Shakespeare's sonnets."
			theFile = 'shakespeare.txt'
		try : 
			theDict = wordFrequencies(theFile)
			goOn = True
		except IOError : 
			print "The filename you entered doesn't seem to exist."
			print "Make sure the file is inside the folder 'poem engine' and include the file extension."
			print "Please enter the filename again."
	goOn = False
	print "What word would you like the poem to begin with?"
	while(goOn == False) : 
		firstWord = raw_input().lower()
		if(firstWord in theDict and firstWord in syllablesDict) : 
			goOn = True
		else : 
			print "Please type a more commonly used word or a word that appears in your sample."
	poem = firstWord + ' '
	firstWordSyllables = syllablesDict.get(firstWord)

	poem += writeLine(firstWord.lower(), theDict, 5 - firstWordSyllables) + '\n'
	poem += writeLine(poem[poem.rfind(' ')+1:-1], theDict, 7) + '\n'
	poem += writeLine(poem[poem.rfind(' ')+1:-1], theDict, 5)
	print "\n" + poem



def isInDict(value, dictionary) : 
	for i in dictionary.values() : 
		if value in i : 
			return True
	return False

def readInSentencePattern(theFile) : 
	sentencePatternList = []
	with open(theFile, 'r') as f : 
		for line in f : 
			sentencePatternList += [line]
	return sentencePatternList


vocab = pickle.load(open('pickled_5000_parts_of_speech.txt','rb'))

themeDict = pickle.load(open('pickled_themeDict.txt','rb'))

def getNumberOfSyllables(Syl_word):
    count = 0
    vowels = 'aeiouy'
    Syl_word = Syl_word.lower()
    if Syl_word[0] in vowels:
        count +=1

    for index in range(1,len(Syl_word)):
        if Syl_word[index] in vowels and Syl_word[index-1] not in vowels:
            count +=1
    if Syl_word.endswith('e'):
        count -= 1
    if Syl_word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
        return count
    

def generateLine(sentencePattern, theme) : 
	bracket = sentencePattern.find('[')
	while(bracket >= 0) : 

		partOfSpeech = sentencePattern[bracket+1]

		if(partOfSpeech == 'N') : 
			candidates = themeDict.get(theme)
		else : 
			candidates = vocab.get(partOfSpeech)
		theWord = candidates[random.randint(0, len(candidates)-1)]
		sentencePattern = sentencePattern[:bracket] + theWord + sentencePattern[bracket+3:]
		bracket = sentencePattern.find('[')
	return (sentencePattern[0].upper() + sentencePattern[1:]).strip()


#haiku
def generatePoem() : 
	print "Please type a theme that is listed below: "
	goOn = False
	while(goOn == False) : 
		themeList = themeDict.keys()
		for a,b,c in zip(themeList[::3],themeList[1::3],themeList[2::3]):
			print '{:<30}{:<30}{:<}'.format(a,b,c)
		theme = raw_input()
		if theme in themeList : 
			goOn = True
		else : 
			print "Please enter the exact name of a listed theme."
	numLines = int(raw_input("How many lines do you want your poem to be?\n"))
	sentencePatternList = readInSentencePattern('sentencePatterns.txt')
	poem = ""
	for i in range(0, numLines) : 
		poem += generateLine(random.choice(sentencePatternList),theme) + "\n"
	print "\n" + poem

def main() : 
	print 'What type of poem would you like to generate? Freeform or haiku?'
	goOn = False 
	while(goOn == False) : 
		poemType = raw_input().lower()
		if(poemType == 'haiku') : 
			goOn = True
			writeHaiku()
		elif(poemType == 'freeform') : 
			goOn = True
			generatePoem()
		else : 
			print "Please enter either 'haiku' or 'freeform'"

main()
