import numpy as np
def modinv(a,m):
    a=a%m
    for x in range(1,m):
        if (a*x)%m==1:
            return x
    raise Exception("No inv")

def hill_encrypt(plaintext,key):
    n=2
    nums=[ord(c)-97 for c in plaintext.lower().replace(" ","")]
    if len(nums)%n: nums += [23]
    mat=np.array(key).reshape(n,n)
    out=""
    for i in range(0,len(nums),n):
        block=np.array(nums[i:i+n])
        enc=(mat.dot(block))%26
        out += "".join(chr(int(x)+97) for x in enc)
    return out

def hill_decrypt(ciphertext,key):
    n=2
    mat=np.array(key).reshape(n,n)
    det=int(round(np.linalg.det(mat)))%26
    invdet=modinv(det,26)
    adj=np.array([[mat[1,1],-mat[0,1],],[-mat[1,0],mat[0,0]]])
    invmat=(invdet*adj)%26
    out=""
    nums=[ord(c)-97 for c in ciphertext]
    for i in range(0,len(nums),n):
        block=np.array(nums[i:i+n])
        dec=(invmat.dot(block))%26
        out += "".join(chr(int(x)%26+97) for x in dec)
    return out

key=[3,3,2,5]
pt="help"
ct=hill_encrypt(pt,key)
dt=hill_decrypt(ct,key)
print(ct)
print(dt)
