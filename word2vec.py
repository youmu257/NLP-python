# !/usr/bin/python3
# coding=utf-8
# reference from https://radimrehurek.com/gensim/models/word2vec.htm,
#                http://zake7749.github.io/2016/08/28/word2vec-with-gensim/
import IO
from gensim.models import Word2Vec

'''
Train word2vec with simple parameter
@param trainFile : input file must be split by space. If data is chinese, you must segment it.
'''
def trainWord2Vec(trainFile):
    sentences = IO.ReadByLine(trainFile)
    sentences = [words.split(' ') for words in sentences]
    print('Read file finish!')
    
    '''
    parameter of Word2Vec
    `sentence`  list   train corpus, a two dimension list
    `sg`        int    defines the training algorithm. Default 0 use CBOW, otherwise 1 use skip-gram.
    `size`      int    is the dimensionality of the feature vectors.
    `window`    int    is the maximum distance between the current and predicted word within a sentence.
    `alpha`     double is the initial learning rate (will linearly drop to `min_alpha` as training progresses).
    `min_count` int    filter words which frequency lower than this.
    `workers`   int    the number of threads to train the model.
    `hs`        int    if 1 use hierarchical softmax for model training, 
                       else 0(default) or `negative` is non-zero use negative sampling.
    `negative`  int    if > 0 use negative sampling , the int is "noise words"(usually between 5-20).
                       Default is 5. If set to 0, no negative samping is used.
    `iter`      int    number of iterations (epochs) over the corpus. Default is 5.
    '''
    model = Word2Vec(sentences, size=250)
    # Save our model.
    model.save("med250.model.bin")


# Train model
# trainWord2Vec("corpus.txt")

# To load a model.
model = Word2Vec.load("med250.model.bin")

s1 = '演員'
s2 = '文學'
s3 = '英語'

res = model.most_similar(s2, topn = 10)
print('%s的前10個相似字\n' % s2, res)

res = model.similarity(s1, s3)
print('%s與%s的相似分數  = ' % (s1, s2), res)

res = model.most_similar([s1, s2], [s3], topn= 10)
print("%s之於%s，如%s之於" % (s1, s3, s2))
print( res)

res = model.most_similar(s1, topn = 10)
print('%s的前10個相似字\n' % s1, res)