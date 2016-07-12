'''
In this project you will experiment with a padding oracle attack against a toy web site hosted 
at crypto-class.appspot.com . Padding oracle vulnerabilities affect a wide variety of products, 
including secure tokens .

This project will show how they can be exploited. We discussed CBC padding oracle attacks in 
week 3 (segment number 5), but if you want to read more about them, please see Vaudenay's paper .

Now to business. Suppose an attacker wishes to steal secret information from our target web site 
crypto-class.appspot.com . The attacker suspects that the web site embeds encrypted customer data 
in URL parameters such as this:

http://crypto-class.appspot.com/po?er=f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4

That is, when customer Alice interacts with the site, the site embeds a URL like this in web 
pages it sends to Alice. The attacker intercepts the URL listed above and guesses that the 
ciphertext following the "po?er=" is a hex encoded AES CBC encryption with a random IV of some 
secret data about Alice's session.

After some experimentation the attacker discovers that the web site is vulnerable to a CBC 
padding oracle attack. In particular, when a decrypted CBC ciphertext ends in an invalid pad 
the web server returns a 403 error code (forbidden request). When the CBC padding is valid, 
but the message is malformed, the web server returns a 404 error code (URL not found).

Armed with this information your goal is to decrypt the ciphertext listed above. To do so 
you can send arbitrary HTTP requests to the web site of the form:

http://crypto-class.appspot.com/po?er="your ciphertext here"

and observe the resulting error code. The padding oracle will let you
decrypt the given ciphertext one byte at a time. To decrypt a single 
byte you will need to send up to 256 HTTP requests to the site. Keep 
in mind that the first ciphertext block is the random IV. The decrypted 
message is ASCII encoded.

To get you started here is a short Python script that sends a ciphertext 
supplied on the command line to the site and prints the resulting error 
code. You can extend this script (or write one from scratch) to implement 
the padding oracle attack. Once you decrypt the given ciphertext, please 
enter the decrypted message in the box below.
script link: 
http://spark-university.s3.amazonaws.com/stanford-crypto/projects/pp4-attack_py.html

This project shows that when using encryption you must prevent padding 
oracle attacks by either using encrypt-then-MAC as in EAX or GCM, or if 
you must use MAC-then-encrypt then ensure that the site treats padding 
errors the same way it treats MAC errors.

'''

import urllib2
import sys
import binascii

TARGET = 'http://crypto-class.appspot.com/po?er='

iv = 'f20bdba6ff29eed7b046d1df9fb70000'
ct = '58b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
pt = ''
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                print "We got: %d" % e.code
                return True # good padding
            return False # bad padding

def iToHex(i):
    result = hex(i)[2:]
    return result.zfill(2)
    
def hex_to_str(a):
    x = a
    result = binascii.unhexlify(x)
    return result.decode('ascii');
    
def xor(a,b):
    b=b[:len(a)]
    result = (int(a,16)^int(b,16))
    strResult = '{:x}'.format(result)
    return strResult.zfill(len(a))
    
'''
if __name__ == "__main__":
    po = PaddingOracle()
    po.query(sys.argv[1])       # Issue HTTP query with the given argument
'''    
def findByte(byte, blockPrev, blockCur):
    length = len(blockPrev) + len(blockCur) - 32
    x = length - 2*byte
    global pt
    i = 0
    pad = iToHex(byte)*byte
    while (i < 256) :
        po = PaddingOracle()
        guess = iToHex(i) + pt
        blockPrevNew = blockPrev[:x]+xor(blockPrev[x:],xor(guess, pad))
        q = blockPrevNew+blockCur
        res = po.query(q)
        if res:
            pt = guess
            break
        i= i+1
    print 'pt: '+pt
    
    
b=1
while b<9:
    findByte(b, iv+ct[:64], ct[64:])
    b = b+1
#something weird happens when the pad is the same as the guess, 
#but the good news is that the pad is known after the first few runs
pt = '090909090909090909'
b = 10
while (b<17):
    findByte(b, iv+ct[:64], ct[64:])
    b = b+1
ptBlock3 = pt
pt = ''
b=1
while(b<17):
    findByte(b, iv+ct[:32], ct[32:64])
    b = b+1
ptBlock2 = pt
pt = ''
b=1
while(b<17):
    findByte(b, iv, ct[:32])
    b = b+1
ptBlock1 = pt

secret = ptBlock1+ptBlock2+ptBlock3[:14]
print hex_to_str(secret)