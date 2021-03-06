# Common NLP tools
Some common used python tool for text pre-processing and NLP tools, including chinese and english.

## Requirement
1. jibea : `pip install jieba`
2. opencc for python, download from [link](https://github.com/yichen0831/opencc-python)
3. NLTK : `pip install nltk`
4. gensim : `pip install gensim`

## Usage
### Prerocessing

1. Chinese segment  
	We use jieba to segment chinese corpus.  
	Command `python ChineseSegment.py input.txt output.txt user_dict(default is None)`  
	to segment a corpus file or reference sample code in your code.

		
		# sample code
		# init jieba
		segment = ChineseSegment()
		# segment = ChineseSegment('data//dictionary//user_dict.dict')
		arr = ['測試','正在測試','今天晚餐吃啥','小明碩士畢業於中國科學院計算所']
		# segment chinese array or string
		print(segment.cut(arr[3]))
		print(segment.cut(arr))
		# segment chinese array or string for search mode
		print(segment.cutForSearch(arr[3]))
		# segment and POStagging input sentence
		print(segment.tokenizer(arr[3]))


2. Conversion in traditional chinese and simplified chinese
	We use opencc in python to convert.  
	Command `python opencc.py input.txt output.txt conversion_model(default=s2t)` 
	to convert a corpus file

3. Common corpus pre-processing
	This tool contain stemming, stopwords, removing punctuation, removing url and convert word to lower case.  
	We adopt `argparse` to execute command. You need input `-i` and `-o` to assign the path of input file and output file. Then, you can choose `-s`, `-p`, `-u` and `-sw` to stemming, filter punctuation, filter url and filter stopwords. If you want to turn on all settings, you can use `-a` parameter.  
	For example, `python Preprocessing.py -i input.txt -o output.txt -a`.  
	We also provide sample code(demo function) in `Preprocessing.py`.

### NLP tool
1. Word2Vec  
	Just a example of how to use wWrd2Vec in `gensim`.
	Word2Vec used to find similar opinion word and word clustering.
	You can reference the code of `word2vec.py` to train a new model and test it. I reference this [website](http://zake7749.github.io/2016/08/28/word2vec-with-gensim/).
	If you need a pre-trained model for english, you can use the [model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) trained by google.
2. Doc2Vec  
	Just a example of how to use Dord2Vec in `gensim`.  
	Doc2Vec used to implement document clustering, support QA sustem, or find similar opinion sentence.
	You can reference the code of `doc2vec.py` to train a new model and test it. I reference this [website](https://radimrehurek.com/gensim/models/doc2vec.html).

## To Do
1. More preprocessing tool, like parse tree, basic statistics, etc.
2. Some example of NLP tools, like topic model, named entity recognition, etc.
