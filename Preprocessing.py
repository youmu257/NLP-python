# !/usr/bin/python3
# -*- coding: utf-8 -*-

from nltk.stem import PorterStemmer
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string, re, argparse

class Preprocessing:
    mode = {
        "stemming" : False,
        "removePunctuation" : False,
        "removeURL" : False,
        "removeStopwords" : False,
        }
    
    def __init__(self, stemming=False, removePunctuation=False, removeURL=False, removeStopwords=False, all=False):
        self.ps = PorterStemmer()
        self.mode["stemming"] = stemming
        self.mode["removePunctuation"] = removePunctuation
        self.mode["removeURL"] = removeURL
        self.mode["removeStopwords"] = removeStopwords
        
        if all:
            for k in self.mode.keys(): self.mode[k]=True
        
    # stemming with PorterStemmer
    # @param text : is a string or string array
    def stem(self, text):
        if type(text) is list:
            result = list()
            for word in text:
                result.append(self.ps.stem(word))
            return result
        else:
            return self.ps.stem(text)
    
    def checkPunt(self, word):
        if len(word) > 0:
            count = 0
            for w in word:
                if w in set(string.punctuation):
                    count+=1
            if count == len(word): 
                return False
            return True
        return False
    
    # removing all punctuation 
    # @param words : a string array 
    def removePunt(self, words):
        return [word for word in words if self.checkPunt(word)]
    
    # remove url
    # @param url : a string
    def removeUrl(self, url):
        # first, find and remove url which contain 'http' but allow without 'www'
        url = re.sub(r'\s*(?:https?://)+(www)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', url).strip()
        # second, find and remove url which contain 'www' but allow without 'http'
        return re.sub(r'\s*(?:https?://)?www(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', url).strip() 
    
    # remove url
    # @param corpus : a string or a string array
    def removeUrlFromCorpus(self, corpus):
        if type(corpus) is list:
            return [self.removeUrl(sent) for sent in corpus]
        else: 
            return self.removeUrl(corpus)
    
    # remove stopewords
    # @param words : a one or two dimension string array
    # @param stopwordFile : user definition stopwords list
    def removeEngStopWords(self, words, *stopwordFile):
        stopwordList = set()
        # load stopwords into a set
        if len(stopwordFile) == 0:
            stopwordList = stopwords.words('english')
        else:
            with open(stopwordFile[0], 'r', encoding='utf-8') as fin:
                for word in fin.read().split('\n'): stopwordList.add(word)
        
        if len(words) > 0 and type(words[0]) is list: # if input is two-dimension string array
            return [[ word for word in sent if word not in stopwordList] for sent in words]
        elif type(words) is list: # if input is a string array 
            return [ word for word in words if word not in stopwordList]
    
    def getSentence(self, corpus):
        if self.mode['removeURL']: self.removeUrlFromCorpus(corpus)
        
        if type(corpus) is list:
            return corpus
        else:
            return sent_tokenize(corpus)
    
    # clean a string with mode setting
    # @param sent : a string
    def cleanSent(self, sent):
        words = word_tokenize(sent.strip())

        if self.mode['removePunctuation']: words = self.removePunt(words)
        if self.mode['removeStopwords']: words = self.removeEngStopWords(words)
        if self.mode['stemming']:
            cleanWords = [self.stem(word.lower()) for word in words]
        else: 
            cleanWords = [word.lower() for word in words]
        
        return cleanWords
    
    # clean a corpus with mode setting
    # @param corpus : a string or a list
    def cleanCorpus(self, corpus):
        sents = self.getSentence(corpus)
        cleanSents = [self.cleanSent(sent) for sent in sents]
        return cleanSents
    
    # clean a corpus with mode setting
    # @param corpus : a string or a list
    def cleanCorpusAndWrite(self, corpus, writer):
        sents = self.getSentence(corpus)
        cleanSents = [self.cleanSent(sent) for sent in sents]

        count = 0
        for sentences in cleanSents:
            writer.write(' '.join(sentences)+'\n')
            if count % 10000 == 0:
                print('以執行' + str(count) + '筆')
                writer.flush()
            count += 1
    
def demo():
    #example
    exampleWords = ["python","pythoner","pythoning","pythoned","pythonly"]
    # Preprocessing with five boolean arguments {stemming, removePunctuation, removeURL,removeStopwords, all}
    # input True is represent you want to implement it
    p = Preprocessing(stemming=True, removePunctuation=True, removeURL=True,removeStopwords=True)
    
    # test stemming
    print('stemming string array')
    print(p.stem(exampleWords))
    
    # remove url
    text = ' hello how are you www.ford.com today www.example.co.jp \n https://www.youtube.com/watch?v=123456'+' https://youmu257.github.io/AboutMe/'+' http://www44.test.com/'
    print('\nremove url\noriginal : '+text, '\nAfter removing url : \n', p.removeUrl(text))
    
    # remove english stopwords
    sent = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
    print('\nremove stop words')
    print('original :\n', word_tokenize(sent))
    print('After :\n', p.removeEngStopWords(word_tokenize(sent)))
    
    #remove all punctuation
    sent = "In no way do you want to glorify violence, but at the same time you can't ignore it, says Sledgehammer Games co-founder Michael Condrey."
    print('\nremove all punctuation')
    print('original :\n', word_tokenize(sent))
    print('After :\n', p.removePunt(word_tokenize(sent)))
    
    
    # test clean one sentence
    sent = "@remy: This is waaaaayyyy too much for you!!!!!! At eight o'clock on Thursday morning Arthur didn't feel very good."
    print('\nclean sentence')
    print(p.cleanSent(sent))
    
    # test clean a corpus
    corpus = "@remy: This is waaaaayyyy too much for you!!!!!! At eight o'clock on Thursday morning Arthur didn't feel very good."
    print('clean corpus')
    print(p.cleanCorpus(corpus))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ADD YOUR DESCRIPTION HERE')
 
    # add parameter
    parser.add_argument('-i', '--input', help='input file name', required=True)
    parser.add_argument('-o', '--output', help='output file name', required=True)
    parser.add_argument('-s', '--stem', help='stemming input file', default=False, action="store_true")
    parser.add_argument('-p', '--punctuation', help='remove all punctuation', required=False, action="store_true")
    parser.add_argument('-u', '--url', help='remove all url first', required=False, action="store_true")
    parser.add_argument('-sw','--stopwords', help='remove all stop words', required=False, action="store_true")
    parser.add_argument('-a', '--all', help='remove all', required=False, action="store_true")
    # parse
    args = parser.parse_args()
    # init preprocessing class
    p = Preprocessing(stemming=args.stem, removePunctuation=args.punctuation, removeURL=args.url, removeStopwords=args.stopwords, all=args.all)
     
    fout =  open(args.output, 'w', encoding='utf-8')
    with open(args.input, 'r', encoding='utf-8') as fin:
        p.cleanCorpusAndWrite(fin.read().split('\n'), fout)
    fout.close()
