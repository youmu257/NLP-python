# !/usr/bin/python3
# coding=utf-8

def ReadByLine(filePath):
    arr = list()
    with open(filePath, 'r', encoding='utf-8') as fin:
        for lin in fin.read().split('\n'):
            arr.append(lin)
    return arr