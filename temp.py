# class Hangman:

#     def __init__(self):
#         self.dict = {}
import operator
    
def guessLetter(sentence, wordCount, letterProb, usedLetters):

    wordLength = len(sentence)
    possibleWords = []
    for word in wordCount:
        if len(word) == wordLength:
            possibleWords.append(word)

    for x in range(wordLength):
        if sentence[x] != "_":
            letter = sentence[x]
            newList = []
            for possible in possibleWords:
                if possible[x] == letter:
                    newList.append(possible)

            possibleWords = newList

    newList = []
    for word in possibleWords:
        can = True
        for x in range(len(word)):
            if sentence[x] == "_":
                if word[x] in usedLetters:
                    can = False
        
        if can:
            newList.append(word)

    possibleWords = newList

    # print("Possible Words:")
    # print(possibleWords)

    if len(possibleWords) > 0:
        maxWord = ""
        maxCount = 0
        maxProb = 0
        maxLetter = ""

        while maxProb == 0:
            maxWord = ""
            maxCount = 0
            maxProb = 0
            maxLetter = ""

            for word in possibleWords:
                if wordCount[word] > maxCount:
                    maxCount = wordCount[word]
                    maxWord = word
            # print(maxWord)
            # print(maxCount)
            # print("______")

            for x in range(len(maxWord)):
                if maxWord[x] not in usedLetters:
                    if letterProb[maxWord[x]] > maxProb:
                        maxProb = letterProb[maxWord[x]]
                        maxLetter = maxWord[x]

            if maxProb == 0:
                possibleWords.remove(maxWord)

        print("Top Word: ", maxWord)
        print("Guessed Letter: ", maxLetter)

    else:
        maxProb = 0
        maxLetter = ""
        for item in letterProb:
            if item not in usedLetters:
                if letterProb[item] > maxProb:
                    maxProb = letterProb[item]
                    maxLetter = item
        
        print("No available words")
        print("Guessed Letter: ", maxLetter)
        
    print("\n")
    return maxLetter

def guessWord(sentence, wordCount, letterProb, usedLetters):

    totalGuesses = 0
    correctGuesses = 0
    wrongGuesses = 0

    blankedSent = ""
    for x in range(len(sentence)):
        blankedSent = blankedSent + "_"

    blankedWords = blankedSent.split(" ")
    # for word in blankedWords:
    while "_" in blankedSent:
        print("Current = ", blankedSent)
        guessedLetter = guessLetter(blankedSent, wordCount, letterProb, usedLetters)
        totalGuesses = totalGuesses + 1
        usedLetters.append(guessedLetter)

        tempBlank = ""
        for x in range(len(sentence)):
            if sentence[x] == guessedLetter:
                tempBlank = tempBlank + guessedLetter
            else:
                tempBlank = tempBlank + blankedSent[x]
        
        if blankedSent == tempBlank:
            wrongGuesses = wrongGuesses + 1
        else:
            correctGuesses = correctGuesses + 1

        blankedSent = tempBlank
    
    print("Word = ", blankedSent)
    print("Total Guesses = ", totalGuesses)
    print("Correct Guesses = ", correctGuesses)
    print("Wrong Guesses = ", wrongGuesses)


def main():
    wordCount = {}
    letterProb = {}
    usedLetters = []
    

    letterProb['a'] = 0.08167
    letterProb['b'] = 0.01492
    letterProb['c'] = 0.02782
    letterProb['d'] = 0.04253
    letterProb['e'] = 0.12702
    letterProb['f'] = 0.02228
    letterProb['g'] = 0.02015
    letterProb['h'] = 0.06094
    letterProb['i'] = 0.06966
    letterProb['j'] = 0.0153
    letterProb['k'] = 0.0772
    letterProb['l'] = 0.04025
    letterProb['m'] = 0.02406
    letterProb['n'] = 0.06749
    letterProb['o'] = 0.07507
    letterProb['p'] = 0.01929
    letterProb['q'] = 0.00095
    letterProb['r'] = 0.05987
    letterProb['s'] = 0.06327
    letterProb['t'] = 0.09056
    letterProb['u'] = 0.02758
    letterProb['v'] = 0.00978
    letterProb['w'] = 0.02360
    letterProb['x'] = 0.00150
    letterProb['y'] = 0.01974
    letterProb['z'] = 0.00074

    sentence = input("Enter a word to guess: ")
    sentence = sentence.lower()

    dictWords = [line.strip('\n') for line in open("dictCount.txt")]
    for dictWord in dictWords:
        keyVal = dictWord.split(' ')
        wordCount[keyVal[0]] = int(keyVal[1])

    tempDict = {}

    guessWord(sentence, wordCount, letterProb, usedLetters)
if __name__ == '__main__':
    main()




    1 4567546