from cs50 import get_string

# Receive a string of text
s = get_string("Text:  ")

letters = 0

# Check if the words is in alphabet and if so add one to letters
for i in range(len(s)):
    if s[i].isalpha():
        letters += 1

# print(f"Letters: {letters}\n")


words = 0
flag = False
# Use a flag to check if a word is in alphabet and comes after a space to add word

for i in range(len(s)):
    if s[i].isalpha() and flag == False:
        flag = True
        words += 1

    elif s[i] == ' ':
        flag = False

# print(f"Words: {words}\n")
# find sentences by checking for periods quetion marks or excalamatiion points
sentences = 0

for i in range(len(s)):
    if s[i] == '.' or s[i] == '?' or s[i] == '!':
        sentences += 1

# print(f"Sentences: {sentence}\n")
# get values that you will plug into the equation and then do the equation to get final grade
    L = 100.0 * letters / words
    S = 100.0 * sentences / words

    initialgrade = 0.0588 * L - 0.296 * S - 15.8

    finalgrade0 = round(initialgrade)

    finalgrade = int(finalgrade0)
# print grade

if finalgrade > 16:
    print("Grade 16+")

elif (finalgrade < 1):

    print("Before Grade 1")

else:

    print(f"Grade {finalgrade}")