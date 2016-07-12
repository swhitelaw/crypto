'''Assignment:
In this project you will implement two encryption/decryption systems, 
one using AES in CBC mode and another using AES in counter mode (CTR). 
In both cases the 16-byte encryption IV is chosen at random and is 
prepended to the ciphertext.

For CBC encryption we use the PKCS5 padding scheme discussed in class (13:50). 
While we ask that you implement both encryption and decryption, we will only 
test the decryption function. In the following questions you are given an AES 
key and a ciphertext (both are hex encoded ) and your goal is to recover the 
plaintext and enter it in the input boxes provided below.

For an implementation of AES you may use an existing crypto library such as 
PyCrypto (Python), Crypto++ (C++), or any other. While it is fine to use the 
built-in AES functions, we ask that as a learning experience you implement 
CBC and CTR modes yourself.
'''

from Crypto import Random
from Crypto.Cipher import AES
import base64
import textwrap
import binascii


BLOCK_SIZE=16

#Question 1
cbcKey1 = "140b41b22a29beb4061bda66b6747e14"
cbcCt1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

def getAES(key):
    cipher = AES.new(key.decode('hex'))
    return cipher

def xor(a,b):
    b=b[:len(a)]
    result = (int(a,16)^int(b,16))
    strResult = '{:x}'.format(result)
    return strResult.zfill(len(a))
    
def hex_to_str(a):
    x = a
    result = binascii.unhexlify(x)
    return result.decode('ascii');
    
def cbcDec(key, CT):
    cipher = getAES(key)
    cipherBlocks = textwrap.wrap(CT, 32)
    iv = cipherBlocks[0]
    PT = ''
    numBlocks = len( CT )/32
    prevBlock = iv
    for i in range(1,numBlocks):
        PT = PT+xor(prevBlock, binascii.hexlify(cipher.decrypt(binascii.unhexlify(cipherBlocks[i]))))
        prevBlock = cipherBlocks[i]
        i = i+1
    return PT;
    
def incCtr(iv):
    nonce = iv[:16]
    return nonce+(hex(int(iv[16:], 16) + 1)[2:]).zfill(16);
    
    
def ctrDec(key, CT):
    orgLen = len(CT) - 32
    #CT = CT + ('0'*(32-len(CT)%32))
    cipher = getAES(key)
    cipherBlocks = textwrap.wrap(CT, 32)
    iv = cipherBlocks[0]
    ivStart = iv
    PT = ''
    numBlocks = len( CT )/32
    for i in range(1,numBlocks+1):
        PT = PT+xor(cipherBlocks[i], binascii.hexlify(cipher.encrypt(binascii.unhexlify(ivStart))))
        ivStart = incCtr(ivStart)
    return PT;

def printCBCMsg(key, CT):
    pt = cbcDec(key, CT)
    print hex_to_str(pt)
    return;
    
def printCTRMsg(key, CT):
    pt = ctrDec(key, CT)
    print hex_to_str(pt)
    return;
    
#Question 1
key1 = "140b41b22a29beb4061bda66b6747e14"
ct1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
printCBCMsg(key1, ct1)

key2 = "140b41b22a29beb4061bda66b6747e14"
ct2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
printCBCMsg(key2, ct2)

key3 = "36f18357be4dbd77f050515c73fcf9f2"
ct3 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
printCTRMsg(key3, ct3)

key4 = "36f18357be4dbd77f050515c73fcf9f2"
ct4 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
printCTRMsg(key4, ct4)
