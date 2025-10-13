import string
def build_map(key):
    letters=string.ascii_lowercase
    mapping={letters[i]:key[i] for i in range(26)}
    inv={v:k for k,v in mapping.items()}
    return mapping,inv

def substitute_encrypt(text,mapping):
    out=""
    for ch in text:
        if ch.isalpha():
            lower=ch.lower()
            enc=mapping[lower]
            out += enc.upper() if ch.isupper() else enc
        else:
            out += ch
    return out

def substitute_decrypt(text,inv):
    out=""
    for ch in text:
        if ch.isalpha():
            lower=ch.lower()
            dec=inv[lower]
            out += dec.upper() if ch.isupper() else dec
        else:
            out += ch
    return out

key="phqgiumeaylnofdxjkrcvstzwb"
mapping,inv=build_map(key)
msg="Welcome to CSE"
enc=substitute_encrypt(msg,mapping)
dec=substitute_decrypt(enc,inv)
print(enc)
print(dec)
