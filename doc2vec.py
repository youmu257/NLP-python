# !/usr/bin/python3
# coding=utf-8
# reference from: https://radimrehurek.com/gensim/models/doc2vec.html
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from gensim.models.keyedvectors import KeyedVectors
import time

          
def read_corpus(fname):
    result = []
    with open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            # For training data, add tags
            result.append( TaggedDocument(line.split(), [i]))
    return result

'''
Train Doc2Vec model with simple parameter
@param trainFile : input file must be split by space. If data is chinese, you must segment it.
                   one line represent one document. if the format is different, you need rewrite read_corpus function.
@param saveModel : the name of Doc2Vec and Word2Vec model
'''
def trainDco2Vec(trainFile, saveModel):
    documents = read_corpus(trainFile)
    print ('Data Loading finish')
    
    """
        `documents` list   train corpuse, a TaggedDocument list.
        `dm`        int    training algorithm. Default 1 use 'distributed memory' (PV-DM), 
                           otherwise 0 is `distributed bag of words` (PV-DBOW).
        `size`      int    dimensionality of the feature vectors.
        `window`    int    is the maximum distance between the current and predicted word within a sentence.
        `alpha`     double is the initial learning rate (will linearly drop to `min_alpha` as training progresses).
        `min_count` int    filter words which frequency lower than this.
        `workers`   int    the number of threads to train the model.
        `iter`      int    number of iterations(epochs) over the corpus. Default is 5 of Word2Vec,
                           but values of 10 or 20 are common in published 'Paragraph Vector' experiments.
        `hs`        int    if 1 use hierarchical softmax for model training, 
                           else 0(default) or `negative` is non-zero use negative sampling.
        `negative`  int    if > 0 use negative sampling , the int is "noise words"(usually between 5-20).
                           Default is 5. If set to 0, no negative samping is used.
        `dbow_words` int   if set to 1 trains word-vectors (in skip-gram fashion) simultaneous with DBOW
                           doc-vector training; default is 0 (faster training of doc-vectors only).
    """
    # build the model
    model = Doc2Vec(documents, dm = 0, alpha=0.25, size= 100, min_alpha=0.025, min_count=0)
     
    # start training
    stime = time.time()
    for epoch in range(2):
        if epoch % 100 == 0:
            print ('Now training epoch %s'%epoch)
            print('spend ', (time.time()-stime), 's')
            stime = time.time()
        model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
    
    model.save(saveModel+'.model')
    # if you want to save binary model, append `binary=True` into parameter
    model.save_word2vec_format(saveModel+'.word2vec')
    print('Train model finish')

# Train Doc2Vec model
trainDco2Vec('wiki100_jieba.txt', 'trained')

# Load Doc2Vec model to test
load_model = Doc2Vec.load('trained.model')
docvecs = load_model.docvecs
print (len(docvecs))

# shows the similar words
print (load_model.most_similar('共同語言'))
# shows the learnt embedding
print (load_model['共同語言'])
# shows the similar docs with id = 2
print (load_model.docvecs.most_similar(2))


# Load Word2Vec model
# In Doc2Vec, save_word2vec_format function save word2vec model is default `binary=False`
# Therefore, we load word2vec model need use KeyedVectors.load_word2vec_format and set `binary=False`
model = KeyedVectors.load_word2vec_format("trained.word2vec", binary=False)
s2 = '文學'
res = model.most_similar(s2, topn = 10)
print('%s的前10個相似字\n' % s2, res)

