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

### If a string is longer than 40 characters, it is garbage
def wordlength(word):
    if len(word) > 40:
        return 1
    else:
        return 0
    
### If a string's ratio of alpanummeric characters to total characters 
### is less than 50%, the string is garbage
def ratio_alphanumeric(word):
    alphanum = 0
    for i in word:
        if i.isalnum():
            alphanum += 1
    ratio = ZeroChecker(alphanum, len(word)) 
    if ratio < 0.5:
        return 1
    else: 
        return 0

### If a string has 4 identical characters in a row, it is garbage
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
           
    if max_count > 3:
        return 1
    else: 
        return 0  
    
### If a string has nothing but alphabetic characters, look at the number
### of consonants and vowels. If the number of one is less than 10% the
### number of the other, then the string is garbage. For example, 10 consonants
### and 1 vowel passess, but 11 consonants and 1 vowel would be removed
### as garbage
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
        if vowels < consonants*0.1:
            return 1
        elif consonants < vowels*0.1:
            return 1
        else:
            return 0  
    else:
        return 0
            
### Strop off the first and last character of a string. If there are two
### distinct punctuation characters in the result, then the string is garbage. 
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
            
    
### If a string begins and ends with a lowercase letter, then if the string 
### contains an uppercase letters anywhere in between, then it is removed
### as garbage. 
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
    
    garbage_count = sum([length, alnu_ratio, identical, con_vow_ratio, punct, upper])
    if garbage_count > 0:
        return 1
    else: 
        return 0
    