# !/usr/bin/python3
# -*- coding: utf-8 -*-
from opencc import OpenCC 
import sys

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python3 " + sys.argv[0] + " input and output corpus file path")
        print("For example : python opencc.py input.txt output.txt conversion_model(default is s2t)")
        exit()
    
    model = {
            'hk2s' : 'Traditional Chinese (Hong Kong standard) to Simplified Chinese',
            's2hk' : 'Simplified Chinese to Traditional Chinese (Hong Kong standard)',
            's2t'  : 'Simplified Chinese to Traditional Chinese',
            's2tw' : 'Simplified Chinese to Traditional Chinese (Taiwan standard)',
            's2twp': 'Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)',
            't2hk' : 'Traditional Chinese to Traditional Chinese (Hong Kong standard)',
            't2s'  : 'Traditional Chinese to Simplified Chinese',
            't2tw' : 'Traditional Chinese to Traditional Chinese (Taiwan standard)',
            'tw2s' : 'Traditional Chinese (Taiwan standard) to Simplified Chinese',
            'tw2sp': 'Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)',
            }
    ConversionsModel = 's2t'
    if len(sys.argv) == 4:
        ConversionsModel = sys.argv[3].replace('\"','').replace('\'','')
    
    # check conversions model
    if ConversionsModel not in model.keys():
        print('Conversions model type error!\nPlease observe the following rules:')
        for k,v in model.items():
            print('- '+k+' : '+v)
        exit()
    
    # start convert Chinese
    openCC = OpenCC(ConversionsModel)
    with open(sys.argv[2], 'w', encoding='utf-8') as fout:
        with open(sys.argv[1], 'r', encoding='utf-8') as fin:
            count = 0
            for lin in fin.read().split('\n'):
                fout.write(openCC.convert(lin)+'\n')
                if count % 10000 == 0:
                    print("已處理 "+str(count)+" 筆")
                    fout.flush()
                count += 1

if __name__ == '__main__':
    main()