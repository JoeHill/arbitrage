# -*- coding: utf-8 -*-
from nltk import tokenize
from nltk.chunk.regexp import RegexpParser
from arbitrage import utils
import re

def __preprocess_sentence(sentence):
    """
    Preprocesses a sentence for the grammar parser. Words are concatenated with their adjoining punctuation marks. This method provides heuristics to recognize those entities prior to processing.
    
    :param str sentence: The sentence to preprocess.
    
    :rtype list(str): The list of proper nouns in the pre-processed sentence and fillers to replace removed, recognized entities without altering the grammatical structure.
    """
    split_sentence = re.split(r"\s+", sentence) 
    list_indicies = utils.comma_delimited_list_indicies(split_sentence)
    if list_indicies: 
        sentences = utils.enumerate_sentence_with_list(split_sentence, list_indicies)
       
    return None


def get_entity_set(string):
    """
    Parses a string into a list of POS tagged tuples. After that parses out all proper nouns. If the NNP is followed by another NNP they are concatenated.
    
    :param str string: The string to parse. It's assumed the string is proper English.
    
    :rtype list(str): The list of proper nouns
    """
    sentences = tokenize.sent_tokenize(string)
    quoted = [ ]
    unquoted = [ ]
    for sentence in sentences:
        if '“' in sentence or '”' in sentence or '"' in sentence:
            quoted.append(sentence)
        else:
            unquoted.append(sentence)
    
    parser = RegexpParser("NP: {<DT>? <JJ>* <NNP>+ <NN>*}") 
    for sentence in unquoted:
        print __preprocess_sentence(sentence)

if __name__ == '__main__':
    fp = open("israeli_strike.txt", "rb")
    article = fp.read()
    get_entity_set(article)

