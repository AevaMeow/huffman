#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter
import heapq
import struct
from bitstring import BitArray
from string import *

class HufTree:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
def genHufCodes(node, code = '', resultDict = None):
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

def bitsToRawBytes(bitStr):
    byte_array = bytearray()
    for i in range(0, len(bitStr), 8):
        byte = bitStr[i:i + 8]
        byte_array.append(int(byte, 2))
    
    return byte_array

def hufDictPacker(hufCodes):
    packedTree = b''
    for byte, code in hufCodes.items():
        packedTree += struct.pack('B', byte)
        packedTree += struct.pack('B', len(code))
        int_code = int(code, 2)
        packedTree += struct.pack('>I', int_code)
    return packedTree


def genEncodedFile(hufCodes, extraBits, rawData):
    packedTree = hufDictPacker(hufCodes)
    treeLen = struct.pack('>H', len(packedTree))

    f = open("encoded", 'wb')
    f.write(treeLen)
    f.write(packedTree)
    f.write(struct.pack('H', extraBits))
    f.write(rawData)
    
def parseTree(encoded):
    treeLen = int.from_bytes(encoded.read(2), byteorder='big') // 6
    hufDeCodes = {}
    for i in range(treeLen):
        byte = int.from_bytes(encoded.read(1), 'little')
        codeLen = int.from_bytes(encoded.read(1), 'little')
        code = ((bin(int((encoded.read(4)).hex(), 16)).removeprefix('0b')).rjust(32, '0'))[-codeLen:]
        hufDeCodes[byte] = code
    return(hufDeCodes)

def parseText(encoded):
    extraBits = int.from_bytes(encoded.read(1), 'little')
    encoded.read(1)
    rawData = encoded.read()
    bitStr = ''
    for i in range(len(rawData)):
        bitStr += (str(bin(rawData[i]).removeprefix('0b'))).rjust(8,'0')
    bitStr = bitStr[:-extraBits]
    return bitStr


if __name__ == "__main__":
    # encode
    source = open('source.txt', mode='rb')
    bytes = source.read()
    source.close()
    bytes_freq = dict(Counter(bytes))
    root = genTree(bytes_freq)
    hufCodes = genHufCodes(root)
    binStr = hufEncode(bytes, hufCodes)
    extraBits = 8 - len(binStr) % 8
    binStr += '0' * extraBits
    rawData = bitsToRawBytes(binStr)
    genEncodedFile(hufCodes, extraBits, rawData)

    # decode
    encoded = open('encoded', 'rb')
    hufDeCodes = parseTree(encoded)
    encodedText = parseText(encoded)