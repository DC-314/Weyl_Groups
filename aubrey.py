#!/usr/bin/python

import hashlib


####################################################################
####################################################################
#                                                                  #                           
#                                                                  #
#                    ELIPTIC CURVE FUCTIONS                        #
#                                                                  #
####################################################################
####################################################################

Pcurve= 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1
N=   0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Acurve =0; Bcurve=7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
GPoint = (Gx,Gy)


def modinv(a,n):
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
          ratio = high/low
          nm, new = hm-lm*ratio, high-low*ratio
          lm, low, hm, high = nm, new, lm, low
    return lm % n
    
    
def ECadd(a,b):
    LamAdd = ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve)) % Pcurve
    x = (LamAdd*LamAdd -a[0]-b[0]) % Pcurve
    y = (LamAdd*(a[0]-x)-a[1]) % Pcurve 
#    print ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve))//Pcurve
    return (x,y)
    
        
def ECdouble(a):
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]),Pcurve)) % Pcurve
    x = (Lam*Lam-2*a[0]) % Pcurve
    y = (Lam*(a[0]-x) - a[1]) % Pcurve  
    return (x,y)
    
     
def EccMultiply(GenPoint,ScalarHex):
 #      if ScalarHex == 0 or ScalarHex => N: raise Exception("Invalid Scalar/Private Key") */
 #        ScalarHex = ScalarHex % N
        ScalarBin = str(bin(ScalarHex))[2:]
        Q=GenPoint
        for i in range (1, len(ScalarBin)):
            Q=ECdouble(Q); 
            if ScalarBin[i] == "1":
                Q=ECadd(Q,GenPoint); 
        return (Q)



####################################################################
####################################################################
#                                                                  #
#                                                                  #
#                     PRIVATE TO PUBLIC KEY                        #
#                                                                  #
####################################################################
####################################################################

print "This program will calculate G.k on the secp256k1 eliptic curve";
print "curve   :   y^2  =  x^3  + 7  mod p "     
print "Constants G and p, can be found inside program\n"
privKey = raw_input("Enter private key, k,  in hex format\n")


publicKey = EccMultiply(GPoint,int(privKey,16))

#print  str(hex(publicKey[0])[2:-1]).zfill(64) + str(hex(publicKey[1])[2:-1]).zfill(64)

print "\nThe point G.k, in hex, under eliptic curve multiplication is :"
print "("+str(hex(publicKey[0])[2:-1]).zfill(64)+","+str(hex(publicKey[1])[2:-1]).zfill(64)+")"



uncompressed_key =  "04" + str(hex(publicKey[0])[2:-1]).zfill(64) + str(hex(publicKey[1])[2:-1]).zfill(64)
print"\nUncompressed key format is"
print uncompressed_key + "\n"


if ((publicKey[1] % 2)==0):
       compressed_key = "02" + str(hex(publicKey[0])[2:-1]).zfill(64)
else:
       compressed_key = "03" + str(hex(publicKey[0])[2:-1]).zfill(64)

print  "Compressed key format is"
print compressed_key + "\n"



####################################################################
####################################################################
#                                                                  #                           
#                                                                  #
#                    PUBLIC KEY TO BITCOIN KEY                     #
#                                                                  #
####################################################################
####################################################################


b58 =  '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n /= 58
    return result
 
def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result
	 
def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count
     
def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return b58[0] * leadingZeros + base58encode(base256decode(result))



ripemd160_uncomp = hashlib.new('ripemd160')
ripemd160_comp = hashlib.new('ripemd160')
ripemd160_uncomp.update(hashlib.sha256(uncompressed_key.decode('hex')).digest())
ripemd160_comp.update(hashlib.sha256(compressed_key.decode('hex')).digest())
print "Ripemd160 of Sha256 of key is"
print ripemd160_uncomp.hexdigest()
print ripemd160_comp.hexdigest() + "\n"


bitcoin_address_uncompressed =  base58CheckEncode(0, ripemd160_uncomp.digest())
bitcoin_address_compressed = base58CheckEncode(0, ripemd160_comp.digest())

print  "Bitcoin address derived from uncompressed key is "
print bitcoin_address_uncompressed + "\n"
print  "Bitcoin address derived from compressed key is "
print bitcoin_address_compressed + "\n"

