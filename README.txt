Hulu Programming Challenge (Hangman Solver)
Atreya Tata


HOW TO RUN:
To run this hangman solver all you have to do is run ./run.sh with the required arguments for the code and number of iterations.



HOW I MADE IT:
To make this hangman solver I realized that I need to make it guess the statistically highest probability for a letter.
To achieve this I collected 3,000 Wikipedia articles on various topics. This serves as a sample for the English language. The implicit
assumption is that this is representative of the English languge. I first sanitized the articles, removing any punctuation or numbers from them
with a Python script I wrote. The script output every single word along with a value of 1 (word count) onto new lines. This would be the inital input
for a MapReduce server. I had previously already built a MapReduce server for another project so I used that server to calculate word counts for 
every unique word in all the articles combined. The results of this are stored in dictCount.txt. There are around 24,000 unique words in there
with their corresponding word counts, together as key-value pairs. Once I had this document of word counts, I read them into a dictionary that
mapped a word to its word count. I also found from the internet the frequencies of letters in the English language. These values have been
hard-coded into my program but can be changed as the user sees fit.

My algorithm firsty splits the phrase into its different words, and does the following on each of the words:
It looks for words of the required length and gradually narrows the search to force certain letters to be in specific positions. It then
finds the word with the highest word count that could possibly be the word currently being focussed on. Then for that highest count word it has found,
it finds the letter, within that word, that has still not been used and has the highest letter frequency. 
For each word in the phrase, I add the best guess letter for each word into a list. I then loop through the list and check which letter occurs most 
often in the list. Ties are broken again in favor for the ltter with the greater letter frequency. The result of this is the final letter that is
guessed by the program.
This process is repeated until the program has either run out of guesses or if it has successfully guessed the complete phrase.



RESULTS:
I ran this program multiple times, each time executing  a large number of loops. The result was that my program is generally able to guess the phrase
within 3 incorrect guesses with around 75% success rate. With some of the phrases, I tried to guess the phrase myself, as a human, and in most cases
the program out performed me which shows that it does work and that the algorithm is effective. I have provided some of the output that came from
running the program on loops of varying numbers. The output shows the progress being made by the program and also shows which letter is guessed on
each iteration. The last line of each iteration specifies whether or not it succeeded. The total successes, failures, and run are given at the
bottom of the files.
A summary is below:
Run 1 (output.txt): 
75 success
25 fail
100 total

Run 2 (output2.txt): 
360 success
140 fail
500 total

Run 3 (outpu3.txt): 
232 success
68 fail
300 total

Run 4 (output4.txt): 
73 success
27 fail
100 total

Run 5 (output5.txt): 
150 success
50 fail
200 total

Sum of all runs:
890 success
310 fail
1200 total


POSSBILE IMPROVEMENTS:
The big assumption in this process is that the Wikipedia articles I downloaded were representative of how words are used in the Enligh language.
This assumption may well be false and to improve results, if there was more time, I would try to find a sample that is more representative. 
Additionally, my program does not take into account how words are used in relation to eachother (if certain words are more likely to follow others).
If there was time to improve my algorithm, this is something I would take into account to make the program think more like a human and favor certain 
words to others based on the other words already revealed in the game.