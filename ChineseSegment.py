# !/usr/bin/python3
# -*- coding: utf-8 -*-

# A simple tool use jieba to segment chinese
# jieba's open source from https://github.com/fxsjy/jieba
# we let default dictionary is bigDictPath('data//dictionary//dict.txt.big')
# if you want to change path, the variable in ChineseSegment class
import jieba, sys, os
import jieba.posseg as pseg

class ChineseSegment:
    # default dictionary for Traditional Chinese
    bigDictPath = 'data//dictionary//dict.txt.big'
    def __init__(self, *userDict):
        if len(userDict) != 0:
            jieba.load_userdict(userDict)
        jieba.set_dictionary(self.bigDictPath)
    
    def cut(self, text ):
        if type(text) is list:
            result = list()
            for s in text:
                result.append(jieba.lcut(s))
            return result 
        else:
            return jieba.lcut(text)
    
    def cutForSearch(self, text ):
        if type(text) is list:
            result = list()
            for s in text:
                result.append(jieba.lcut_for_search(s))
            return result 
        else:
            return jieba.lcut_for_search(text)
    
    # Segment and POStagging input sentence
    # return [pari(word, tagging)]
    def tokenizer(self, text):
        if type(text) is list:
            result = list()
            for s in text:
                result.append(pseg.lcut(s))
            return result 
        else:
            return pseg.lcut(text)

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python3 " + sys.argv[0] + " input and output corpus file path")
        print("For example : python ChineseSegment.py input.txt output.txt user_dict(default is None)")
        exit()
    
    # check user dictionary is exits
    userDict = ''
    if len(sys.argv) == 4:
        if os.path.isfile(sys.argv[3]):
            userDict = sys.argv[3]
        else:
            print('User dictionary not found!\nUsing default dictionary only.')
    
    # start segment corpus 
    with open(sys.argv[2], 'w', encoding='utf-8') as fout:
        with open(sys.argv[1], 'r', encoding='utf-8') as fin:
            if len(userDict) > 0:
                #append user dictionary into model
                segment = ChineseSegment(sys.argv[3])
            else:
                segment = ChineseSegment()
            
            count = 0
            for lin in fin.read().split('\n'):
                fout.write(' '.join(segment.cut(lin))+'\n')
                if count % 10000 == 0:
                    fout.flush()
                    print('已執行 '+str(count)+'次')
                count+=1
                
if __name__ == "__main__":
#     main()
#     '''
    # sample code
    
    segment = ChineseSegment()
#     segment = ChineseSegment('dictionary//dict.txt.big')
    arr = ['測試','正在測試','今天晚餐吃啥','小明碩士畢業於中國科學院計算所']
#     print(segment.cut(arr[3]))
#     print(segment.cut(arr))
#     print(segment.cutForSearch(arr[3]))
    print(segment.tokenizer(arr[3]))
#     '''