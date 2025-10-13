# ecc_demo_fixed_run.py
# ECC toy demo (educational). Uses small parameters and simple EC-ElGamal.
# Not secure — for learning only.

def mod_pow(a, e, m):
    r = 1 % m
    a %= m
    while e:
        if e & 1:
            r = (r * a) % m
        a = (a * a) % m
        e >>= 1
    return r

def inv_mod(a, m):
    # Fermat's little theorem (m must be prime here)
    return mod_pow((a % m + m) % m, m - 2, m)

class Point:
    def __init__(self, x=None, y=None, inf=False):
        self.x = x
        self.y = y
        self.inf = inf  # True if "point at infinity"

    def __repr__(self):
        return "Infinity" if self.inf else f"({self.x},{self.y})"

class Curve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, P):
        if P.inf:
            return True
        lhs = (P.y * P.y) % self.p
        rhs = (P.x * P.x * P.x + self.a * P.x + self.b) % self.p
        return lhs == rhs

    def add(self, P, Q):
        if P.inf:
            return Q
        if Q.inf:
            return P
        pmod = self.p
        # P + (-P) = O
        if P.x == Q.x and (P.y + Q.y) % pmod == 0:
            return Point(inf=True)

        if P.x == Q.x and P.y == Q.y:
            num = (3 * P.x * P.x + self.a) % pmod
            den = (2 * P.y) % pmod
        else:
            num = (Q.y - P.y) % pmod
            den = (Q.x - P.x) % pmod

        # If denominator is 0 mod p, inv_mod will attempt inv of 0 -> returns something wrong.
        # We'll catch ZeroDivision-like issues by testing den % p
        if den % pmod == 0:
            return Point(inf=True)
        lam = (num * inv_mod(den, pmod)) % pmod
        xr = (lam * lam - P.x - Q.x) % pmod
        yr = (lam * (P.x - xr) - P.y) % pmod
        return Point(xr, yr)

    def scalar_mul(self, P, k):
        R = Point(inf=True)
        A = P
        n = k
        while n:
            if n & 1:
                R = self.add(R, A)
            A = self.add(A, A)
            n >>= 1
        return R

def encode_message_to_x(msg: str, p: int):
    """Encode message into integer x (big-endian). Return (x, lossy_flag)."""
    x = 0
    for c in msg:
        x = (x << 8) + ord(c)
    if x >= p:
        return x % p, True
    return x, False

def decode_x_to_message(x_val: int):
    """Decode integer back to bytes (big-endian)."""
    if x_val == 0:
        return '\x00'
    bytes_list = []
    rx = x_val
    while rx > 0:
        bytes_list.append(chr(rx & 0xFF))
        rx >>= 8
    bytes_list.reverse()
    return ''.join(bytes_list)

def find_y_for_x(x_val, a, b, p):
    """Brute-force search for y in [0..p-1] such that (x, y) is on curve."""
    rhs = (x_val * x_val * x_val + a * x_val + b) % p
    for y in range(p):
        if (y * y) % p == rhs:
            return y
    return None

def main():
    print("ECC demo (small parameters) using curve y^2 = x^3 + a*x + b (mod p)")
    p = 9739
    a = 497
    b = 1768
    curve = Curve(a, b, p)
    print(f"Params: p={p}, a={a}, b={b}")

    # Generator point
    G = Point(1804, 5368)
    if not curve.is_on_curve(G):
        print("Generator not on curve. Exiting.")
        return

    # Key generation (demo)
    dA = 6534  # private key A
    dB = 8742  # private key B
    QA = curve.scalar_mul(G, dA)
    QB = curve.scalar_mul(G, dB)

    print(f"Public QA = dA*G = {QA}")
    print(f"Public QB = dB*G = {QB}")

    # Input message
    msg = input("Enter a short message (<=6 chars recommended): ")
    x_raw, lossy = encode_message_to_x(msg, p)
    if lossy:
        print("Warning: encoded integer >= p, value reduced modulo p (this loses information).")
    x = x_raw % p

    # find y such that (x, y) on curve
    y_found = find_y_for_x(x, a, b, p)
    if y_found is None:
        print("Failed to find a y for the chosen x (mod p). Try a different (shorter) message.")
        return

    M = Point(x, y_found)
    print(f"Message encoded as point M={M} (x mod p = {x})")

    # Encryption using B’s public key (EC-ElGamal)
    k = 1234  # ephemeral key (demo)
    C1 = curve.scalar_mul(G, k)
    kQB = curve.scalar_mul(QB, k)
    C2 = curve.add(M, kQB)
    print(f"Ciphertext: C1={C1}, C2={C2}")

    # Decryption by B
    dB_C1 = curve.scalar_mul(C1, dB)
    neg = Point(dB_C1.x, (p - dB_C1.y) % p)
    recovered = curve.add(C2, neg)

    if recovered.inf:
        print("Recovered point is point at infinity — decryption failed.")
        return

    print(f"Recovered point: {recovered}")
    recovered_msg = decode_x_to_message(recovered.x)
    print(f"Recovered message (decoded from x): {recovered_msg!r}")

    if recovered.x == M.x and recovered.y == M.y:
        print("Point recovered matches original encoded point (success).")
    else:
        print("Recovered point differs from original encoded point (possible encoding lossy or different y chosen).")

    print("\nNote: toy demo. Real ECC uses proper point encoding schemes (no lossy modulo), standard curves, and secure ephemeral keys.")

if __name__ == "__main__":
    main()