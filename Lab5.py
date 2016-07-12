'''
Your goal this week is to write a program to compute discrete log modulo a prime p. 
Let g be some element in Z*p and suppose you are given h in Z*p such that h=gx where 
x between 0 and 2^40. Your goal is to find x. More precisely, the input to your program is p,g,h 
and the output is x.

The trivial algorithm for this problem is to try all 240 possible values of x until
the correct one is found, that is until we find an x satisfying h=gx in Zp. This 
requires 240 multiplications. In this project you will implement an algorithm that 
runs in time roughly 2^20 using a meet in the middle attack.

Let B=220. Since x is less than B2

we can write the unknown x base B as x=x0*B+x1





By moving the term gx1 to the other side we obtain

  h/g^x1=(g^B)^x0   in Zp.

The variables in this equation are x0,x1 and everything else is known: you are given g,h and B=220. 
Since the variables x0 and x1 are now on different sides of the equation we can find a solution 
using meet in the middle (Lecture 3.3 at 14:25):

First build a hash table of all possible values of the left hand side h/gx1 for x1=0 to 2^20
Then for each value x0=0 to 2^20 check if the right hand side (gB)x0 is in this hash table. 
If so, then you have found a solution (x0,x1) from which you can compute the required x as x=x0B+x1.
The overall work is about 220 multiplications to build the table and another 220 lookups in this table.

Now that we have an algorithm, here is the problem to solve:

p=13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171

h=11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568

g=3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333

Each of these three numbers is about 153 digits. Find x such that h=gx in Zp.

To solve this assignment it is best to use an environment that supports multi-precision and modular arithmetic. In Python you could use the gmpy2 or numbthy modules. Both can be used for modular inversion and exponentiation. In C you can use GMP. In Java use a BigInteger class which can perform mod, modPow and modInverse operations.

'''

import numpy as np


p=long(13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171)

       
g=long(11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568)

       
h=long(3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333)

def extEuclideanAlg(a, b) :
    """
    Computes a solution  to a x + b y = gcd(a,b), as well as gcd(a,b)
    """
    if b == 0 :
        return 1,0,a
    else :
        x, y, gcd = extEuclideanAlg(b, a % b)
        return y, x - y * (a // b),gcd
 
def modinv(a,m) :
    """
    Computes the modular multiplicative inverse of a modulo m,
    using the extended Euclidean algorithm
    """
    x,y,gcd = extEuclideanAlg(a,m)
    if gcd == 1 :
        return x % m
    else :
        return None

def createHash(g, h, p):
    d = {}
    for xOne in range (1,2**20+1):
        num = np.mod(np.multiply(h, modinv(pow(g, xOne, p), p)), p)
        d[num] = xOne
    return d
    
def findVal(g,h,p):
    B = 2**20
    d = createHash(g,h,p)
    print len(d)
    xZero= 0
    xOne=0
    for i in range (1,2**20+1):
        num = pow(g,np.multiply(B,i),p)
        if d.has_key(num):
            xZero=i
            xOne=d[num]
            break
        i = i+1
    result = np.multiply(xZero,B)+xOne 
    print result
    

#print modinv(7, 23)
#print np.(g,p)
findVal(g,h,p)
