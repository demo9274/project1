def simple_encrypt(text, key):
    cipher_text = ""
    for i in range(len(text)):
        cipher_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return cipher_text

def simple_decrypt(cipher_text, key):
    plain_text = ""
    for i in range(len(cipher_text)):
        plain_text += chr(ord(cipher_text[i]) ^ ord(key[i % len(key)]))
    return plain_text

key = "8bytekey"
msg = "Meet me very urgently"

ct = simple_encrypt(msg, key)
pt = simple_decrypt(ct, key)

print("Cipher Text (unreadable):", ct)
print("Decrypted Text:", pt)
