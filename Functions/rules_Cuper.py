import pandas as pd
import sklearn
import csv
import string
import unicodedata
from sklearn.feature_extraction.text import strip_accents_unicode
import numpy as np

def trim_word(word, from_start=0, from_end=0):
    return word[from_start:len(word) - from_end]

def ZeroChecker(character,word_length):
    ## This function returns the ratio of a character type in a word
        if word_length != 0:
            result = character / word_length
        else:
            result = 0
        return result

### if a string is more than 18 characters in length, it is garbag
def wordlength(word):
    if len(word) > 18:
        return 1
    else:
        return 0
    
### if a word contains more than one punctuation characte
def punctuation(word):
    word_punc = word
    punctuation = len([letter for letter in word_punc if unicodedata.category(letter).startswith("P")])
    if punctuation > 0:
        return 1
    else:
        return 0
    
### If there are three or more identical characters in a row in a string, it is garbage
def identical_chars(word):
    check_char = ""
    same_count = 1
    max_count = 1
    
    for char in word:
        if char == check_char:
            same_count += 1
            if same_count > max_count:
                max_count = same_count
        else:
            check_char = char
            same_count = 1 
           
    if max_count > 2:
        return 1
    else: 
        return 0  

### If all the characters in a string are alphabetic, and if the ratio of vowels to consonants is larger than 2, or the ratio of consonants to vowels is larger than 4, or ir there are no vowels or no consonants  present, it is garbage. 
def ratio_cons_vowels(word, consonants_list, vowels_list):
    if word.isalpha():
        vowels = 0
        consonants = 0
        word = strip_accents_unicode(word)
        
        for char in word:
            if char in vowels_list:
                vowels += 1
            elif char in consonants_list:
                consonants += 1
        
        vowel_consonant_ratio = ZeroChecker(vowels,consonants)
        consonant_vowel_ratio = ZeroChecker(consonants,vowels)
        
        if vowel_consonant_ratio == 0 or vowel_consonant_ratio >= 2 :
            return 1
        elif consonant_vowel_ratio == 0 or consonant_vowel_ratio >= 4:
            return 1
        else:
            return 0  
    else:
        return 0


### if the word is not fully uppercase, and the word contains an uppercase character that is not the first character, it is garbage
def uppercase(word):
    if word.isupper():
        return 0
    elif not (word[1:]).islower():
        return 1
    else:
        return 0        


## If there are three or more consecutive vowels in the string or five or 
## more consecutive consonants in the string or if it contains no vowels, it is garbage. 
def consecutive_chars(word, consonants_list, vowels_list): 
    char_token = None
    count = 1
    max_consecutive_consonants = 0
    max_consecutive_vowels = 0
    word = strip_accents_unicode(word)
    word = word.lower()
    
    for letter in word:
        if letter in consonants_list:
            char_type = 1
        elif letter in vowels_list:
            char_type = 0
        else:
            char_type = None
        
        if char_type == char_token:
            count += 1
        else:
            char_token = char_type
            count = 1 
        if char_type == 1 and count > max_consecutive_consonants:
            max_consecutive_consonants = count
        if char_type == 0 and count > max_consecutive_vowels:
            max_consecutive_vowels = count
    if max_consecutive_vowels < 1:
        return 1
    elif (max_consecutive_vowels >= 3) or (max_consecutive_consonants >= 5):
        return 1
    else:
        return 0            
    

### if a word consists of less than 70% dutch letters, it is garbage
def dutch_characters(word, dutch_char_list):
    word_length = len(word)
    dutch_letters = len([letter for letter in word if letter in dutch_char_list])    
    if dutch_letters < word_length:
        return 1
    else:
        return 0

## if a word contains a number, it is garbage
def numbers_count(word):
    for i in word:
        if i.isnumeric():
            return 1
        else:
            return 0
            
## if a word contains an accent:
##def accents_count(word, accents_list):
##   accents = len([letter for letter in word if letter in accents_list])   
##   if accents > 0:
##        return 1
##    else:
##        return 0

### if a word contains other characters than alphanumeric or punctuation it is garbage
##def other_characters(word):
##   other_characters = len([letter for letter in word if not ##unicodedata.category(letter).startswith("P") if not letter.isalnum()])
##   if other_characters > 0:
##        return 1
##    else:
 ##       return 0

    
### A main function to check if a word is garbage or not.
### A word is considered as garbage when at least one function return a 1
def Main(word, consonants_list, vowels_list, dutch_char_list, accents_list):
    length = wordlength(word)
    identical = identical_chars(word)
    con_vow_ratio = ratio_cons_vowels(word, consonants_list, vowels_list)
    punct = punctuation(word)
    upper = uppercase(word)
    consecutive = consecutive_chars(word, consonants_list, vowels_list)
    dutch = dutch_characters(word, dutch_char_list)
    numbers = numbers_count(word)

    
    garbage_count = sum([length, identical, con_vow_ratio, punct, upper, consecutive, dutch, numbers])
    if garbage_count > 0:
        return 1
    else: 
        return 0