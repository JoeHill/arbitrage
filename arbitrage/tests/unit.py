from unittest import TestCase
import re

from arbitrage import utils

from nose.tools import ok_, eq_

class TestUtils( TestCase ):

  def setUp( self ):
    self.sentence_with_list = re.split( r"\s+", "This is a sentence listing igloos, aardvarks, vestiges, and boolean." )
    self.sentence_with_two_lists = re.split( r"\s+", "This is a sentence listing igloos, aardvarks, vestiges, and boolean, but it also lists the carribean, shoes, hats, and gloves." )

    # Source: http://www.eslbee.com/sentences.htm
    # A simple sentence, also called an independent clause, contains a subject and a verb, and it expresses a complete thought
    self.simple1 = "Alicia goes to the library and studies every day.".split( ' ' ) # s: Alicia v: goes, studies
    self.simple2 = "Juan and Arturo play football every afternoon.".split( ' ' ) # s: Juan, Arturo v: play
    self.simple3 = "Some students like to study in the mornings.".split( ' ' ) # s: students, v: like 

    # A compound sentence contains two independent clauses joined by a coordinator. The coordinators are as follows: for, and, nor, but, or, yet, so. Except for very short sentences; coordinators are always preceded by a comma.
    self.compound1 = "I tried to speak Spanish, and my friend tried to speak English.".split( ' ' ) # s: I, friend c: , and v: tried, tried 
    self.compound2 = "Alejandro played football, so Maria went shopping.".split( ' ' ) # s: Alejandro, Maria c: , so v: played, went
    self.compound3 = "Alejandro played football, for Maria went shopping.".split( ' ' ) # s: Alejandro, Maria c: , for v: played, went

    # A complex sentence has an independent clause joined by one or more dependent clauses. A complex sentence always has a subordinator such as because, since, after, although, or when or a relative pronoun such as that, who, or which
    self.complex1 = "When he handed in his homework, he forgot to give the teacher the last page.".split( ' ' ) # s: he, he v: handed, forgot, sub: When, (comma after homeword)
    self.complex2 = "The teacher returned the homework after she noticed the error.".split( ' ' ) # s: teacher, she v: returned, noticed sub: after
    self.complex3 = "The students are studying because they have a test tomorrow.".split( ' ' ) # s: students, they v: are studying, have sub: because
    self.complex4 = "After they finished studying, Juan and Maria went to the movies.".split( ' ' ) # s: They, Juan, Maria v: finished, went sub: After, (comma after studying)
    self.complex5 = "Juan and Maria went to the movies after they finished studying.".split( ' ' ) # s: Juan, Maria, they v: went, finished sub: after

    # sentences containing adjective clauses (or dependent clauses) are also complex because they contain an independent clause and a dependent clause.
    self.complex_adj_clause1 = "The woman who called my mom sells cosmetics.".split( ' ' ) # s: woman, v: sells sub: who, ic: The woman, sells cosmetics
    self.complex_adj_clause2 = "The book that Jonathan read is on the shelf.".split( ' ' ) # s: book v: is sub: that ic: The book, is on the shelf
    self.complex_adj_clause3 = "The house which Abraham  Lincoln was born in is still standing.".split( ' ' ) # s: house v: is sub: which ic: The house, is still standing
    self.complex_adj_clause4 = "The town where I grew up is in the United States.".split( ' ' ) # s: town v: is sub: where ic: The town, is in the United States


  def test_comma_delimited_list_indicies( self ):
    first_indicies = utils.comma_delimited_list_indicies( self.sentence_with_list )
    second_indicies = utils.comma_delimited_list_indicies( self.sentence_with_two_lists )
    eq_( first_indicies[0], set( [ 5, 6, 7 ] ) )
    eq_( second_indicies[0], set( [ 5, 6, 7 ] ) )
    eq_( second_indicies[1], set( [ 16, 17, 15 ] ) )


  def test_filter_punctuation( self ):
    a = utils.filter_punctuation( self.sentence_with_list )
    b = utils.filter_punctuation( self.sentence_with_two_lists )
    eq_( a, "This is a sentence listing igloos aardvarks vestiges and boolean".split( ' ' ) )
    eq_( b, "This is a sentence listing igloos aardvarks vestiges and boolean but it also lists the carribean shoes hats and gloves".split( ' ' ) )

  def test_enumerate_sentence_with_list( self ):
    #first_indicies = utils.comma_delimited_list_indicies( self.sentence_with_list )
    second_indicies = utils.comma_delimited_list_indicies( self.sentence_with_two_lists )
    
    #print utils.enumerate_sentence_with_list( self.sentence_with_list, first_indicies )
    sens = utils.enumerate_sentence_with_list( self.sentence_with_two_lists, second_indicies )
    
    eq_( sens[ 0 ], ['This', 'is', 'a', 'sentence', 'listing', 'vestiges', 'and', 'boolean,', 'but', 'it', 'also', 'lists', 'the', 'hats', 'and', 'gloves.'] )
    eq_( sens[ 1 ], ['This', 'is', 'a', 'sentence', 'listing', 'aardvarks', 'and', 'boolean,', 'but', 'it', 'also', 'lists', 'the', 'shoes', 'and', 'gloves.'] )
    eq_( sens[ 2 ], ['This', 'is', 'a', 'sentence', 'listing', 'igloos', 'and', 'boolean,', 'but', 'it', 'also', 'lists', 'the', 'carribean', 'and', 'gloves.'] )

  def test_is_compound_sentence( self ):
    ok_( utils.is_compound_sentence( self.compound1 ) ) 
    ok_( utils.is_compound_sentence( self.compound2 ) ) 
    ok_( not utils.is_compound_sentence( self.simple1 ) ) 
    ok_( not utils.is_compound_sentence( self.simple2 ) ) 
