import pandas as pd
import sklearn
import csv
import string
import unicodedata
from sklearn.feature_extraction.text import strip_accents_unicode

## define functions
def ZeroChecker(character_count,word_length):
    ## This function returns the ratio of a character type in a word
        if word_length != 0:
            result = character_count / word_length
        else:
            result = 0
        return result
    
def CharacterCounts(word, vowels_list, consonants_list, punctuation_list, dutch_char_list, accents_list):
    ## This function returns the amount of times a certain character type occurs in a word 
  
    # Determine word length
    word_length = len(word) 
   
    # Count the amount of vowels, independent of accents or commonness in Dutch
    vowels = len([letter for letter in strip_accents_unicode(word) if letter in vowels_list])
    word_vowel_ratio = ZeroChecker(vowels,word_length)

    # Count the amount of consonants, independent of accents or commonness in Dutch
    consonants = len([letter for letter in strip_accents_unicode(word) if letter in consonants_list])
    word_consonant_ratio = ZeroChecker(consonants,word_length)
    
    # Determine the amount of consonants and vowels, independent of accents or commonness in Dutch
    vowelandconsonant = vowels+consonants
    word_vowelandconsonant_ratio = ZeroChecker(vowelandconsonant,word_length)
    
    # Count the amount of punctuation marks in a word
    punctuation = len([letter for letter in word if unicodedata.category(letter).startswith("P")])
    word_punctuation_ratio = ZeroChecker(punctuation,word_length)

    # Count the amount of Dutch letters 
    dutch_chars = len([letter for letter in word if letter in dutch_char_list])    
    word_dutch_chars_ratio = ZeroChecker(dutch_chars,word_length)

    # Count the amount of upper case characters, excluding the first character
    if word.isupper():
        upper = word_length
    else: 
        upper = len([letter for letter in word[1:] if letter.isupper()])
    word_uppercase_ratio = ZeroChecker(upper,word_length )      
    
    # Count the amount of lower case characters
    lower = len([letter for letter in word if letter.islower()])
    word_lowercase_ratio = ZeroChecker(lower,word_length)
    
    # Count the amount of numbers
    numbers = len([letter for letter in word if letter.isnumeric()])
    word_numbers_ratio = ZeroChecker(numbers,word_length)
    
    # Count the amount of alphanumeric characters
    alpha = len([letter for letter in word if letter.isalpha()])
    word_alpha_ratio = ZeroChecker(alpha, word_length)

    # Count the amount of accented characters
    accents = len([letter for letter in word if letter in accents_list])   
    word_accents_ratio = ZeroChecker(accents,word_length)
    
    # Number of other characters
    other_characters = len([letter for letter in word if not unicodedata.category(letter).startswith("P") if not letter.isalnum()])
    word_other_characters_ratio = ZeroChecker(other_characters, word_length)

    # ratio of vowels to consonants
    word_vowels_consonant_ratio = ZeroChecker(vowels,consonants)
    word_consonant_vowels_ratio = ZeroChecker(consonants,vowels)

    return [word_length,
            vowels,
            consonants,
            vowelandconsonant,
            punctuation,
            dutch_chars,
            upper,
            lower,
            numbers,
            alpha, 
            accents,
            other_characters,
            word_vowel_ratio,
            word_consonant_ratio,
            word_vowelandconsonant_ratio,
            word_punctuation_ratio,
            word_dutch_chars_ratio,
            word_uppercase_ratio,
            word_lowercase_ratio,
            word_numbers_ratio,
            word_alpha_ratio,
            word_accents_ratio,
            word_other_characters_ratio,
            word_vowels_consonant_ratio,
            word_consonant_vowels_ratio]
    
def consecutiveSameCharacter(word):
    ## this function returns the maximum numbers of time a character occurs consecutivly in a word
    check_char = ""
    same_count = 1
    max_count_same_char = 0

    for letter in word:
        if letter == check_char:
            same_count += 1
        else:
            check_char = letter
            same_count = 1 
        if same_count > max_count_same_char:
            max_count_same_char = same_count

    return max_count_same_char
    
def consecutiveStrippedSameCharacter(word):
    ## this function returns the maximum numbers of time a character occurs consecutivly in a word independent of accents and case
    check_char = ""
    same_count = 1
    max_count_strip_same_char = 0
    word = strip_accents_unicode(word)
    word = word.lower()
    
    for letter in word:
        if letter == check_char:
            same_count += 1
        else:
            check_char = letter
            same_count = 1 
        if same_count > max_count_strip_same_char:
            max_count_strip_same_char = same_count
    
    return max_count_strip_same_char

def consecutiveCharacters(word,vowels_list,consonants_list):
    ## this function returns the maximum numbers of times a type of character occurs consecutivly in a word, independent of accents and case 
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

    return max_consecutive_consonants, max_consecutive_vowels

def Main(garbagelist, vowels_list, consonants_list, dutch_char_list, punctuation_list, accents_list):
    ## This function combines all of the above functions and returns a list of lists of all characteristics of every word in the set
    colnameslist = ["word",
                "word_length",
                "vowels",
                "consonants",
                "vowelandconsonant",
                "punctuation",
                "dutch_char",
                "upper",
                "lower",
                "numbers",
                "alpha",
                "accents",
                "other_characters",
                "word_vowel_ratio",
                "word_consonant_ratio",
                "word_vowelandconsonant_ratio",
                "word_punctuation_ratio",
                "word_dutch_char_ratio",
                "word_uppercase_ratio",
                "word_lowercase_ratio",
                "word_numbers_ratio",
                "word_alpha_ratio",
                "word_accents_ratio",
                "word_other_characters_ratio",
                "word_vowels_consonant_ratio",
                "word_consonant_vowels_ratio",
                "max_count_same_char", 
                "max_count_strip_same_char",
                "max_consecutive_consonants",
                "max_consecutive_vowels"]
    characteristics_total = []
    
   # for word in garbagelist:       
    for word in garbagelist:
 
        
        # collect the amount of times a certain character type occurs in a word and their ratios
        characteristics_list = CharacterCounts(word, vowels_list, consonants_list, punctuation_list, dutch_char_list, accents_list)
        # collect the highest amount of consecutive characters for each word
        max_count_same_char = consecutiveSameCharacter(word)
        max_count_strip_same_char = consecutiveStrippedSameCharacter(word)
        max_consecutive_consonants, max_consecutive_vowels = consecutiveCharacters(word,vowels_list,consonants_list)
        # append the characteristics to the characteristics_list
        characteristics_list.extend([max_count_same_char,
                                     max_count_strip_same_char,
                                     max_consecutive_consonants,
                                     max_consecutive_vowels])
        # insert word and garbage score
        characteristics_list[0:0] = [word]
        
        # append the characteristics list of each word to the total list
        characteristics_total.append(characteristics_list)
        
    feature_scores_df = pd.DataFrame(characteristics_total, columns = colnameslist)
        
    return feature_scores_df