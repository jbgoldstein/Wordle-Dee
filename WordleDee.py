#Import necessary modules
import pandas as pd
import re
from random import randrange

#Import helper functions
from WDFunctions import loadWordList, evaluateLetters, eliminateLetters

#Instructions and Input
print("Instructions: Enter all guessed words seperated by a space.")
print("Mark yellow letters with a question mark (?) following the letter.")
print("Mark green letters with an exclaimation point (!) following the letter.")
print("For a starting word, input the word 'none'.")
word_input = input("Enter guessed words here:").lower()

#Start by looking at all already guessed words
guessed_words = word_input.lower().translate({ord("?"): None, ord("!"): None}).split(" ")

#Logic for when determining potential next guesses
if(guessed_words[0] != "none"):
    
    #If letters are green or yellow, keep them in mind for later
    green_letters, yellow_letters = evaluateLetters(word_input)
    
    #If letter isn't green or yellow, then it shouldn't been in the word
    eliminated_letters = eliminateLetters(word_input, green_letters, yellow_letters)
    
    #Start thinking about potential words
    initial_list = loadWordList()
    
    #If a word has already been guessed, eliminate the possibility
    unguessed_words = initial_list[~initial_list["Potential Words"].isin(guessed_words)]
    
    #If a word contains letters that we know are neither yellow or green, eliminate the possibility
    no_eliminated_letters = unguessed_words[unguessed_words["Potential Words"].apply(lambda word: 1 not in [letter in word for letter in eliminated_letters])]
    
    #If a word does not contain all known yellow letters, eliminate the possibility
    has_yellow_letters = no_eliminated_letters[no_eliminated_letters["Potential Words"].apply(lambda word: 0 not in [letter in word for letter in yellow_letters])]
    
    #If a word does not contain known green letters in the exact position, eliminate the possibility
    remaining_possibilities = has_yellow_letters[has_yellow_letters["Potential Words"].apply(lambda word: re.match(''.join(list(green_letters.values())), word) != None)]
    
#Seperate logic for determining potential start word
else:
    #Think of potential starting words
    remaining_possibilities = loadWordList()

#Prioritize common words. If stumped, use any word that comes to mind
if(remaining_possibilities["Potential Words"].size > 10):
    most_common_words = remaining_possibilities.sort_values(by=["Usage Frequency", "Vowel Count"], ascending = False).head(round(remaining_possibilities["Potential Words"].size * .10))
else:
    most_common_words = remaining_possibilities.sort_values(by=["Usage Frequency", "Vowel Count"], ascending = False)
    
#Prioritize unique letters in early guesses
if(guessed_words[0] == "none" or len(guessed_words) < 3):
    unique_letters = most_common_words[most_common_words["Unique Letters"].apply(lambda unique_letter_value: unique_letter_value == most_common_words["Unique Letters"].max())]
else:
    unique_letters = most_common_words

#Prioritize using more vowels in early guesses
if(guessed_words[0] == "none" or len(guessed_words) < 3):
    final_list = unique_letters[unique_letters["Vowel Count"].apply(lambda vowel_count_value: vowel_count_value == unique_letters["Vowel Count"].max() or vowel_count_value == unique_letters["Vowel Count"].max() - 1)]
else:
    final_list = unique_letters

#With list of potential options in mind, randomly pick from options to take your guess
selected_word = final_list["Potential Words"].values[randrange(0, final_list["Potential Words"].size)]

#Input word and see results
print("Suggested Next Word: " + selected_word)