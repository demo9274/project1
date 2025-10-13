def encrypt(text,key1,key2):
    res=""
    for i in range(len(text)):
        c=ord(text[i])^ord(key1[i%len(key1)])
        c=c^ord(key2[i%len(key2)])
        res+=chr(c)
    return res
def decrypt(text,key1,key2):
    res=""
    for i in range(len(text)):
        c=ord(text[i])^ord(key2[i%len(key2)])
        c=c^ord(key1[i%len(key1)])
        res+=chr(c)
    return res
key1="firstkey"
key2="secondky"
msg="welcome to cse"
enc=encrypt(msg,key1,key2)
dec=decrypt(enc,key1,key2)
print(enc)
print(dec)
