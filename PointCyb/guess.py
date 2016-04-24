#!/usr/bin/python2
import sys, random, math

maxNumber = random.randint(1, 10000)
minNumber = random.randint(1, maxNumber)
maxTries = int(math.log(maxNumber-minNumber, 2) + 1)
toGuess = random.randint(minNumber, maxNumber)

print("You'll have up to %s tries to find a number between %s and %s" % (maxTries, minNumber, maxNumber))
guess = 0
tries = 0
while tries < maxTries and guess != toGuess:
    guess = int(input("Give a number to guess between %s and %s: " % (minNumber, maxNumber)))
    tries += 1
    if guess > toGuess:
        print("Too high !")
    elif guess < toGuess:
        print("Too low !")

#print("Guess = %s, ToGuess = %s, Tries = %s, MaxTries = %s" % (guess, toGuess, tries, maxTries))
if guess == toGuess:
    print("Congratulations, you won in %s tries, it was %s !" % (tries, toGuess))
else:
    print("You lost, retry in less than %s attempts." % maxTries)
