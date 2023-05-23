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

### If a string is more than 20 characters in length, it is garbage
def wordlength(word):
    if len(word) > 20:
        return 1
    else:
        return 0
    
### Taghva: If a string's ratio of alpanummeric characters to total characters 
### is less than 50%, the string is garbage
### Kulp: If the number of punctuation characters in a string is greater than the number of alphanumeric characters, it is
### garbage
def ratio_alphanumeric(word):
    alphanum = 0
    punctuation = 0
    for char in word:
        if char.isalnum():
            alphanum += 1
        if unicodedata.category(char).startswith("P"):
            punctuation += 1
    if punctuation > alphanum:
        return 1
    else: 
        return 0
    
### gnoring the first and last characters in a string, if there are two or 
### more different punctuation characters in the string, it is garbage 
def punctuation(word):
    punct_count = 0
    punct_list = []
    word = trim_word(word, 1, 1)
    for char in word:
        if unicodedata.category(char).startswith("P"):
            if char not in punct_list:
                punct_list.append(char)
                punct_count += 1
    if punct_count > 1:
        return 1
    else: 
        return 0 
    
### f there are three or more identical characters in a row in a string, it is garbage
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
    
##  If the number of uppercase characters in a string is greater than the number of 
### lowercase characters, and if the number of uppercase characters is less 
### than the total number of characters in the string, it is garbage   
def upper_ratio(word):
    lower = 0
    upper = 0
    total_len = len(word)
    for char in word:
        if char.islower():
            lower += 1
        if char.isupper():
            upper += 1
    if upper > lower:
        if upper < total_len:
            return 1
        else:
            return 0
    else:
        return 0
        
### If all the characters in a string are alphabetic, and if the number of consonants in the string is greater than 8
### times the number of vowels in the string, or vice-versa, it is garbage. 
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
        if vowels < consonants*0.125:
            return 1
        elif consonants < vowels*0.125:
            return 1
        else:
            return 0  
    else:
        return 0
            
## If there are four or more consecutive vowels in the string or five or 
## more consecutive consonants in the string, it is garbage. 
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

    if (max_consecutive_vowels >= 4) or (max_consecutive_consonants >= 5):
        return 1
    else:
        return 0            
    
### If the first and last characters in a string are both lowercase and any other character is uppercase,
def uppercase(word):
    if ((word[0].islower()) & (word[-1].islower())):
        if not word.islower():
            return 1
        else: 
            return 0
    else:
        return 0        
    
    
### A main function to check if a word is garbage or not.
### A word is considered as garbage when at least one function return a 1
def Main(word, consonants_list, vowels_list):
    length = wordlength(word)
    alnu_ratio = ratio_alphanumeric(word)
    identical = identical_chars(word)
    con_vow_ratio = ratio_cons_vowels(word, consonants_list, vowels_list)
    punct = punctuation(word)
    upper = uppercase(word)
    upper_r = upper_ratio(word)
    consecutive = consecutive_chars(word, consonants_list, vowels_list)
    
    garbage_count = sum([length, alnu_ratio, identical, con_vow_ratio, punct, upper, upper_r, consecutive])
    if garbage_count > 0:
        return 1
    else: 
        return 0