def dels(x: int) -> set[int]:
    dividers = set()
    for d in range(1, int(x ** .5) + 1):
        if x % d == 0:
            dividers.add(d)
            dividers.add(x // d)
    return set(sorted(list(dividers)))


p, q = 157, 433
n = p * q
n_1 = (p - 1) * (q - 1)
dels_n_1 = dels(n_1)
e = 3467  # random.randint(1000, 10000)
dels_e = dels(e)
d = 15395

while list(dels_n_1 & dels_e) != [1]:
    e += 1
    dels_e = dels(e)

while ((e * d) % n_1) != 1:
    d += 1


def encrypt(raw):
    encrypted = ""
    for c in raw:
        encrypted += chr(ord(c) ** e % n)
    return encrypted


def decrypt(enc):
    decrypted = ""
    for c in enc:
        decrypted += chr(ord(c) ** d % n)
    return decrypted


inp = "hello world"
print(enc := encrypt(inp))
print(decrypt(enc))
print(decrypt(enc) == inp)
