# -*- coding: utf-8 -*-
"""
The code  returns a set of words that appear
in at least 4 senti-sentences

Created on Fri Sep 23 12:14:49 2016

@author: Vivek
"""

import re
import time
from nltk.corpus import stopwords
import urllib2
from operator import itemgetter

"""
Loads a Lexicon from a text file
"""
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

"""
The run function accepts the path to
a local file  as a parameter and returns a set with all the words that
appear in at least 4 senti-sentences in the file. 
"""
def run(path):
   #load the positive and negative lexicons
   posLex=loadLexicon('positive-words.txt')
   negLex=loadLexicon('negative-words.txt')

   freq={}
   finalset=set()
   sentidict=set() # set of senti-sentences
   
   stopLex=set ( stopwords.words('english'))

   

   #If file is not read properly
   
   success=False# become True when we get the file
   
   for i in range(5): # try 5 times
      try:
         #use the browser to access the url
         fin=open(path)
         success=True # success
         break # we got the file, break the loop
	  
      except:# browser.open() threw an exception, the attempt to get the response failed
		  print 'failed attempt',i


   # all five attempts failed, return  None
   if not success: return None
   

   text=fin.read()

   sentences=text.split('.')

   for sentence in sentences: # for each sentence

       sentence=sentence.lower().strip() # lower case and strip

       sentence=re.sub('[^a-z]',' ',sentence) # replace all non-letter characters  with a space

       words=sentence.split(' ') # split to get the words in the sentence

       for word in words: # for each word in the sentence

                if word in posLex or word in negLex:
                        sentidict.add(sentence) #stores words with sentiments in sentidict
                        break


   for sentence in sentidict: # for each sentence
                print sentence
                sentence=sentence.lower().strip() # loewr case and strip

                sentence=re.sub('[^a-z]',' ',sentence) # replace all non-letter characters  with a space

                words=sentence.split(' ') # split to get the words in the sentence
                
                wordset=set()
                
                for word in words: # for each word in the sentence

                        if word=='' or word in stopLex or word in posLex or word in negLex:continue # ignore empty words and stopwords

                        else: wordset.add(word) # update the frequency of the word
                
                for word in wordset:
                    freq[word]=freq.get(word,0)+1 #stores word and count in freq dictionary
                    

   #print 'finalset'
   for word in freq:
       
       #print word, freq[word]
       if freq[word] >= 4:
           finalset.add(word)

   fin.close()#close opened file
   return(finalset)

#Code to test run function
if __name__=='__main__':
    print run("textfile.txt")
    
