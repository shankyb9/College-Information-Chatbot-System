


# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:07:51 2018

@author: Group-1
"""

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import (stopwords)
from nltk.stem import WordNetLemmatizer
from nltk.corpus.reader.wordnet import Synset
 
class Sent_Similarity:
    
    def __init__(self):
        
        self.ensw = []
        pass
    
    def penn_to_wn(self,tag):
        """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
        if tag.startswith('N'):
            return 'n'
     
        if tag.startswith('V'):
            return 'v'
     
        if tag.startswith('J'):
            return 'a'
     
        if tag.startswith('R'):
            return 'r'
     
        return None
     
    def tagged_to_synset(self,word, tag):
        wn_tag = self.penn_to_wn(tag)
        if wn_tag is None:
            return word
     
        try:
            syn = wn.synsets(word, wn_tag)
            if(syn):
                return syn[0] 
            else:
                return word
        except:
            return None
     
        
    def find_lemma(self, word, tag):
        lemmatizer=WordNetLemmatizer()
        lem = lemmatizer.lemmatize(word, tag)
        return lem, tag 
    
    
    def sentence_similarity(self,sentence1, sentence2):
        """ compute the sentence similarity using Wordnet """
        
        # making similarity check case insensitive
        sentence1 = sentence1.lower()
        sentence2 = sentence2.lower()
        # Tokenize and tag
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))
        
        # remove stopwords and then find similarity between sentences
        sentence1 = self.removeStopWords(sentence1)
        sentence2 = self.removeStopWords(sentence2)
     
        # Get the synsets for the tagged words
        synsets1 = [self.tagged_to_synset(*tagged_word) for tagged_word in sentence1]
        synsets2 = [self.tagged_to_synset(*tagged_word) for tagged_word in sentence2]
     
        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss]
        synsets2 = [ss for ss in synsets2 if ss]
     
        score, count = 0.0, 0
     
        # For each word in the first sentence
        for synset in synsets1:
            #        print([synset.path_similarity(ss) for ss in synsets2])
            #         Get the similarity value of the most similar word in the other sentence
            list_similarity = [0]
            for ss in synsets2:
                try:
                    sim =synset.wup_similarity(ss) # or path_similarity
                except:
                    if(str(ss)==str(synset) and ss==synset):
                        sim=1.0
                    elif(type(ss)!=type(synset)):
                        if(type(ss)==str and type(synset)==Synset and wn.synsets(ss,synset.pos())!=[]):
                            sim = synset.wup_similarity(wn.synsets(ss,synset.pos())[0])
                        elif(type(synset)==str and type(ss)==Synset and wn.synsets(synset,ss.pos())!=[]):
                            sim = ss.wup_similarity(wn.synsets(synset,ss.pos())[0])
                        else:
                            sim = 0.0
                    else:
                        sim = 0.0
                if(sim!=None):
                    list_similarity.append(sim) 
            best_score = max(list_similarity)
     
            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
                count += 1
     
        # Average the values
        if count==0:
            count=1 # to prevent divide by 0 error
        score /= count
        return score
     
    
        
    def symmetric_sentence_similarity(self,sentence1, sentence2):
        """ compute the symmetric sentence similarity using Wordnet """
        # can remove stopwords if wanting so
        return (self.sentence_similarity(sentence1, sentence2) + self.sentence_similarity(sentence2, sentence1)) / 2 
     
        
    def ini_stopwords(self):
        # choosing stopwords
        self.ensw = stopwords.words('english')
        # creating our own stopwords list
        add_ensw = ['provide','about']
        for w in add_ensw:
            self.ensw.append(w)
        self.ensw.remove('be')
        self.ensw.remove('not')
#        print(ensw)
        
    def removeStopWords(self, para):
        
#        pararr=word_tokenize(para)
        #print(pararr)
        
        filterarr=[item for item in para if item[0] not in self.ensw]
#        print(filterarr)
        return filterarr
    

    

