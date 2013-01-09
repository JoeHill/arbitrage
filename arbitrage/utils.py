import re

def comma_delimited_list_indicies( split_sentence ):
  """
  Determines if the sentence has a list of nouns separated by commas (which throw off pos tagging).
  A list of nouns separated by commas is characterized by two or more consecutive words with 
  trailing commas.
  
  :param list(str) split_sentence: The sentence to check, pre-split into a list of it's words.

  :rtype list(int): A list of indicies where list words occur in the split_sentence 
  """
  list_component_indicies = set( ) 
  lists = [ ]
  for i in range(len(split_sentence)):
    if i == 0:
      continue
    else:
      words = split_sentence[i-1:i+1]
      commas = "".join( split_sentence[i-1:i+1] ).count( ',' )
      if commas == 2:
        list_component_indicies.add( i )
        list_component_indicies.add( i - 1 )
      else:
        if list_component_indicies:
          lists.append( set( list_component_indicies ) )
          list_component_indicies = set()
 
  if lists:
    return lists 
  return [] 

def filter_punctuation( split_sentence ):
  """
  Removes the sort of punctuation that causes problem in parsing. This includes the period at the 
  end of sentences, commas, colons, and semi-colons. 
  
  :param list(str) split_sentence: The sentence to clean, pre-split into a list of it's words.

  :rtype list(str): The cleaned, split sentence 
  """
  sentence = " ".join( split_sentence ).replace( ',', '' ).replace( ';', '' ).replace( ':', '' )
  if sentence[-1] == '.':
    sentence = sentence[0:-1]
  return sentence.split( ' ' )

class SentenceWithList:
  """
  Represents a sentence with one or more nested noun lists. Acts as an iterator for the smallest set of enumerated simple sentences.
  """
  def __init__( self, split_sentence, list_indicies_sets ):
    f = lambda a, b : list( a ) + list( b )
  
    list_indicies_lists = [ ]
    for l in list_indicies_sets:
      lst = list( l )
      lst.sort()
      list_indicies_lists.append( lst )

    self.__sentence     = split_sentence
    self.__indicies     = list_indicies_lists 
    self.__placeholders = [ l[0] for l in list_indicies_lists ]
    self.__flattened    =  reduce( f, self.__indicies )
    self.__last_one     = False

  def update_iteration_state( self ):
    ok = False
    if self.__last_one:
      raise StopIteration
    for l in self.__indicies:
      if len( l ) is not 1:
        ok = True
    if not ok:
      self.__last_one = True

  def get_placeholder_indicies( self ):
    words = [ ]

    self.update_iteration_state( )

    for l in self.__indicies:
      if len( l ) > 1:
        word = l.pop()
      else:
        word = l[0]
      words.append( word )
    words.reverse()
    return words

  def next(self):
    sentence = [ ]
    i        = 0

    inds = self.get_placeholder_indicies( )

    while i < len( self.__sentence ):
      incd = False
      if i in self.__flattened:
        sentence.append( self.__sentence[ inds.pop() ].replace( ',', '' ) )
        while i in self.__flattened:
          incd = True
          i = i + 1
      else:
        sentence.append( self.__sentence[ i ] )
      if not incd:
        i = i + 1

    return sentence
  
  def __iter__( self ):
    return self

def enumerate_sentence_with_list( split_sentence, list_indicies ):
  """
  Enumerates a sentence with a list. This occurs by creating a new sentence for every word in the 
  list based on the premise a single word in a list has the same pos as every other word in the list.
  This should allow more accurate pos tagging.

  :param list(str) split_sentence: The sentence to enumerate, pre-split into a list of it's words.

  :rtype list(list(str)): A list of split_sentences
  """
  if not list_indicies:
    return [split_sentence]
  s = SentenceWithList( split_sentence, list_indicies )
  sentences = [ ]
  for sentence in s:
    sentences.append( sentence )
  return sentences

def has_subordinator( split_sentence ):
  sentence = " ".join( split_sentence )
  subordinators = set( [ "although", "though", "even though", "while", "whereas", "as", 
  "as though", "than", "like", "just as", "since", "so that", "because", "if", "in case", 
  "in order for", "unless", "after", "as", "before", "by the time", "ever since", 
  "every time", "once", "whether", "when", "until", "whenever", "before", "anytime", 
  "if", "as if", "whether", "unless", "wherever", "where", "how", "even if", "even though", 
  "except that", "except if", "not only", "what", "where", "who", "whom", "whose", 
  "whenever", "wherever", "whatever" ] )
  for subordinator in subordinators:
    if subordinator in sentence:
      return True
  return False

def has_non_list_comma( split_sentence ):
  list_indicies   = comma_delimited_list_indicies( split_sentence )
  split_sentences = enumerate_sentence_with_list( split_sentence, list_indicies ) 
  is_in = 0
  for split_sentence in split_sentences:
    if ',' in "".join( split_sentence ):
      is_in = is_in + 1
  if is_in == len( split_sentences ):
    return True
  return False

def has_comma_coordinator( split_sentence ):
  """
  Indicates if the sentence has a comma followed by a coordinator.
  
  :param list(str) split_sentence: The split sentence

  :rtype bool:
  """
  coordinators = [ "for", "and", "nor", "but", "or", "yet", "so" ]
  s = " ".join( split_sentence )
  for c in coordinators:
    if ', ' + c in s:
      return True
  return False
  
def is_compound_sentence( split_sentence ):
  """
  Takes a sentence assumed to be a compound sentence and enumerates it to simple sentences.

  :param list(str) split_sentence: The sentence split as an array.

  :rtype list(list(str)): A list of simple sentences.
  """
  ss = split_sentence
  print " ".join( split_sentence )
  non_list_comma = has_non_list_comma( ss )
  if non_list_comma:
    if has_comma_coordinator( ss ) or has_subordinator( ss ):
      print "A compound sentence."
      return True
  print "Not a compound sentence." 
  return False

def resolve_singular_first_person_pronouns_to_anaphora( split_sentence ):
  """
  Takes a sentence with pronouns and resolves them to their corresponding anaphora.
  
  :param list(str) split_sentence:

  :rtype list(str): The split_sentence with no pronouns.
  """
  pronouns = [ "i", # I -> Subject
               "me", # Me -> Object
               "my", # My -> Possessive determiner
               "mine", # Mine -> Possessive Pronoun
               "myself" ] # Myself -> Reflexive

def resolve_singular_second_person_pronouns_to_anaphora( split_sentence ):
  """
  Takes a sentence with pronouns and resolves them to their corresponding anaphora.
  
  :param list(str) split_sentence:

  :rtype list(str): The split_sentence with no pronouns.
  """
  pronouns = [ "you",       # You -> Subject/Object
               "your",      # Your -> Possessive determiner
               "yours",     # Yours -> Possessive pronoun
               "yourself" ] # Yourself -> Reflexive
  
def resolve_singular_third_person_pronouns_to_anaphora( split_sentence ):
  """
  Takes a sentence with pronouns and resolves them to their corresponding anaphora.
  
  :param list(str) split_sentence:

  :rtype list(str): The split_sentence with no pronouns.
  """
  pronouns = [ "he", "she", 
               "him", "her", 
               "his", "hers", 
               "himself", "herself", 
               "it", 
               "its", 
               "itself" ]

def split_complex_sentence( split_sentence ):
  """
  Takes a sentence with a comma coordinator or a comma and subordinator and splits it appropriately
  into it's simple sentence components.

  :param list(str) split_sentence:

  :rtype list(list(str)): The simple sentence components

  """


