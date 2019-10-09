import json
import urllib.request
import sys
    
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

    maxWord = ""
    maxCount = 0
    maxProb = 0
    maxLetter = ""

    if len(possibleWords) > 0:

        while maxProb == 0:
            maxWord = ""
            maxCount = 0
            maxProb = 0
            maxLetter = ""

            for word in possibleWords:
                if wordCount[word] > maxCount:
                    maxCount = wordCount[word]
                    maxWord = word

            for x in range(len(maxWord)):
                if maxWord[x] not in usedLetters:
                    if letterProb[maxWord[x]] > maxProb:
                        maxProb = letterProb[maxWord[x]]
                        maxLetter = maxWord[x]

            if maxProb == 0:
                possibleWords.remove(maxWord)

        # print("Top Word: ", maxWord)
        # print("Guessed Letter: ", maxLetter)

    else:
        for item in letterProb:
            if item not in usedLetters:
                if letterProb[item] > maxProb:
                    maxProb = letterProb[item]
                    maxLetter = item
        
        # print("No available words")
        # print("Guessed Letter: ", maxLetter)
        
    output = []
    output.append(maxLetter)
    output.append(maxCount)
    output.append(maxWord)

    # return maxLetter
    return output

# def guessWord(sentence, wordCount, letterProb, usedLetters):

#     totalGuesses = 0
#     correctGuesses = 0
#     wrongGuesses = 0

#     blankedSent = ""
#     for x in range(len(sentence)):
#         if sentence[x] == " ":
#             blankedSent = blankedSent + " "
#         else:
#             blankedSent = blankedSent + "_"

#     blankedWords = blankedSent.split(" ")

#     words = sentence.split(" ")

#     for i in range(len(blankedWords)):
#         while "_" in blankedWords[i]:
#             print("Current Word = ", blankedWords[i])
#             print("Current Sentence = ", blankedSent)
#             guessedLetter = guessLetter(blankedWords[i], wordCount, letterProb, usedLetters)[0]
#             totalGuesses = totalGuesses + 1
#             usedLetters.append(guessedLetter)

#             for j in range(len(blankedWords)):
#                 temp = ""
#                 for x in range(len(blankedWords[j])):
#                     if words[j][x] == guessedLetter:
#                         temp = temp + guessedLetter
#                     else:
#                         temp = temp + blankedWords[j][x]
                
#                 blankedWords[j] = temp
                    
#             tempBlank = ""
#             for x in range(len(sentence)):
#                 if sentence[x] == guessedLetter:
#                     tempBlank = tempBlank + guessedLetter
#                 else:
#                     tempBlank = tempBlank + blankedSent[x]
            
#             if blankedSent == tempBlank:
#                 wrongGuesses = wrongGuesses + 1
#             else:
#                 correctGuesses = correctGuesses + 1

#             blankedSent = tempBlank

#         print("Word Complete: ", blankedWords[i])
#         print("\n")

#     print("Sentence Complete: ", blankedSent)
#     print("Total Guesses: ", totalGuesses)
#     print("Correct Guesses: ", correctGuesses)
#     print("Wrong Guesses: ", wrongGuesses)

def guess(sentence, wordCount, letterProb, usedLetters):

    temp = sentence.replace("-", " ")
    sentence = temp

    words = sentence.split(" ")

    suggestedLetters = []
    for word in words:
        if "_" in word:
            # result = guessLetter(word, wordCount, letterProb, usedLetters)
            # usedLetters.append(result[0])
            # print(result[0])
            # print(result[1])
            # print(result[2])
            # return result[0]

            suggestedLetters.append(guessLetter(word, wordCount, letterProb, usedLetters))
    
    highestCount = 0
    highestLetter = ""
    highestProb = 0

    for x in suggestedLetters:
        count = 0
        letter = x[0]
        for y in suggestedLetters:
            if x[0] == y[0]:
                count = count + 1
        
        if count > highestCount:
            highestCount = count
            highestLetter = letter

    if highestCount == 1:
        for x in suggestedLetters:
            if x[1] > highestCount:
                highestCount = x[1]
                highestLetter = x[0]

    usedLetters.append(highestLetter)
    # print(highestLetter)
    # print(highestCount)
    return highestLetter


def main():
    wordCount = {}
    letterProb = {}

    letterProb['A'] = 0.08167
    letterProb['B'] = 0.01492
    letterProb['C'] = 0.02782
    letterProb['D'] = 0.04253
    letterProb['E'] = 0.12702
    letterProb['F'] = 0.02228
    letterProb['G'] = 0.02015
    letterProb['H'] = 0.06094
    letterProb['I'] = 0.06966
    letterProb['J'] = 0.0153
    letterProb['K'] = 0.0772
    letterProb['L'] = 0.04025
    letterProb['M'] = 0.02406
    letterProb['N'] = 0.06749
    letterProb['O'] = 0.07507
    letterProb['P'] = 0.01929
    letterProb['Q'] = 0.00095
    letterProb['R'] = 0.05987
    letterProb['S'] = 0.06327
    letterProb['T'] = 0.09056
    letterProb['U'] = 0.02758
    letterProb['V'] = 0.00978
    letterProb['W'] = 0.02360
    letterProb['X'] = 0.00150
    letterProb['Y'] = 0.01974
    letterProb['Z'] = 0.00074
    letterProb['\''] = 0.00000

    dictWords = [line.strip('\n') for line in open("dictCount.txt")]
    for dictWord in dictWords:
        keyVal = dictWord.split(' ')
        wordCount[keyVal[0]] = int(keyVal[1])

    correct = 0
    wrong = 0
    total = 0

    code = sys.argv[1]
    iterations = int(sys.argv[2])


    # TESTING WITH HULU STUFF
    print("\n")
    for x in range(iterations):
        print("Round ", total + 1)
        usedLetters = []

        data = {}
        with urllib.request.urlopen("http://gallows.hulu.com/play?code="+code) as url:
            data = json.loads(url.read().decode())
            print(data)
            print("\n")
        
        token = data["token"]

        while data["status"] == "ALIVE":
            # print("**********")
            result = guess(data["state"], wordCount, letterProb, usedLetters)
            print("Letter Guessed: ", result)
            with urllib.request.urlopen("http://gallows.hulu.com/play?code="+code+"&token="+token+"&guess="+result) as url:
                data = json.loads(url.read().decode())
                print(data)
                print("\n")

            # print("**********")

        if data["status"] == "FREE":
            correct = correct + 1
            print("Success: ", data["state"])
        if data["status"] == "DEAD":
            wrong = wrong + 1
            print("Fail: ", data["state"])

        print("\n")
        print("\n")
        total = total + 1

    print("Total Success = ", correct)
    print("Total Failures = ", wrong)
    print("Total Attempts = ", total)
    print("\n")
    
    # TESTING LOCALLY
    # usedLetters = []
    # sentence = "ILLUSTRATION PLAN OF A ROOM"
    # guessWord(sentence, wordCount, letterProb, usedLetters)


if __name__ == '__main__':
    main()
