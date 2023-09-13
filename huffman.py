#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter
import heapq

class HufTree:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
def genHufCodes(node, code='', resultDict=None):
    if resultDict is None:
        resultDict = {}
        
    if node is not None:
        if node.char is not None:
            resultDict[node.char] = code
        genHufCodes(node.left, code + '0', resultDict) # рекурсивный обход
        genHufCodes(node.right, code + '1', resultDict)
    return resultDict

def hufEncode(data, hufCodes):
    byteList = [byte for byte in data]
    str1 = ''

    for byte in byteList:
        str1 += hufCodes.get(byte, '')
    
    return str1

def genTree(bytes_freq):
    tree = [ HufTree(char, freq) for char, freq in bytes_freq.items() ]
    heapq.heapify(tree) # доп эффективность

    while len(tree) > 1:
        left = heapq.heappop(tree)
        right = heapq.heappop(tree)
        merge = HufTree(None, left.freq + right.freq)
        merge.left = left
        merge.right = right
        heapq.heappush(tree, merge)
    
    return tree[0]

if __name__ == "__main__":
    source = open('source.txt', mode='rb')
    bytes = source.read()
    source.close()
    bytes_freq = dict(Counter(bytes))
    root = genTree(bytes_freq)
    hufCodes = genHufCodes(root)
    encodedFile = hufEncode(bytes, hufCodes)
    # print(bytes)
    # print(huffman_codes)
    print(encodedFile)
    # запаковать