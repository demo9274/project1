def caesar_encrypt(text, shift):
    result=""
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            result += chr((ord(ch)-ord(base)+shift)%26 + ord(base))
        else:
            result += ch
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

msg="Meet me very urgently"
enc=caesar_encrypt(msg,3)
dec=caesar_decrypt(enc,3)
print("Encription:",enc)
print("Secryption",dec)
