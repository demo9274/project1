def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    for i in range(1, phi):
        if (e * i) % phi == 1:
            return i

p = 11
q = 13
n = p * q
phi = (p - 1) * (q - 1)
e = 7
d = mod_inverse(e, phi)

msg = 9
print("Public Key (e, n):", e, n)
print("Private Key (d, n):", d, n)

cipher = (msg ** e) % n
plain = (cipher ** d) % n

print("Original Message:", msg)
print("Encrypted Message:", cipher)
print("Decrypted Message:", plain)
