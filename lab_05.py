import random
import time

import sympy


def gen_eds_params(blp: int = 512, blq: int = 256) -> tuple[int, int, int, int, int]:
    q = sympy.randprime(2 ** (blq - 1), 2 ** blq)
    p = 0
    while True:
        k_range = 2 ** (blp - blq)
        k = random.randint(k_range, k_range * 2)
        p_candidate = k * q + 1
        if p_candidate.bit_length() != blp:
            continue
        if sympy.isprime(p_candidate):
            p = p_candidate
            break
    while True:
        h = random.randint(2, p - 2)
        a = pow(h, (p - 1) // q, p)
        if a != 1:
            break
    x = random.randint(2, q - 1)
    y = pow(a, x, p)
    return p, q, a, x, y


def get_eds(m: str) -> tuple[int, int]:
    h = custom_hash(m) % q
    if h == 0:
        h = 1

    while True:
        k = random.randint(2, q - 1)

        r = pow(a, k, p)
        r1 = r % q
        if r1 == 0:
            continue

        s = (x * r1 + k * h) % q
        if s == 0:
            continue

        return r1, s


def verify_eds(m: str, r1: int, s: int) -> bool:
    h = custom_hash(m) % q
    if h == 0:
        h = 1
    v = pow(h, q - 2, q)
    z1 = (s * v) % q
    z2 = ((q - r1) * v) % q
    u = (pow(a, z1, p) * pow(y, z2, p)) % p % q
    return u == r1


def custom_hash(o: str) -> int:
    if strategy == 1:
        return ''.join(format(ord(c), '08b') for c in o).count('1')
    elif strategy == 2:
        return sum([ord(c) for c in o]) % pow(2, 16)
    else:
        data = o.encode('utf-8')
        state = 0
        for i in range(0, len(data), 2):
            byte1 = data[i]
            if i + 1 < len(data):
                byte2 = data[i + 1]
            else:
                byte2 = 0
            block = (byte2 << 8) | byte1
            state = (state ^ block) & 0xFFFF
            state = ((state >> 1) | (state << 15)) & 0xFFFF
        return state

strategy = 1
p, q, a, x, y = gen_eds_params(blp=512, blq=256)
message = "Hello world"
ss = 0
n = 10_000
for _ in range(n):
    start = time.time()
    r1_m, s_m = get_eds(message)
    ss += time.time() - start
print(ss)
ss = 0
for _ in range(n):
    start = time.time()
    verify_eds(message, r1_m, s_m)
    ss += time.time() - start
print(ss)
#
# print("Первый случай: ничего не изменено")
# print(f"Сообщение: {message}")
# print(f"Подпись: {r1_m} {s_m}")
# print(f"Действительна ли подпись? {verify_eds(message, r1_m, s_m)}")
# print()
# print("Второй случай: изменено сообщение")
# print(f"Сообщение: {message}1")
# print(f"Подпись: {r1_m} {s_m}")
# print(f"Действительна ли подпись? {verify_eds(message + "1", r1_m, s_m)}")
# print()
# print("Третий случай: изменена первая часть подписи")
# print(f"Сообщение: {message}")
# print(f"Подпись: {r1_m + 100} {s_m}")
# print(f"Действительна ли подпись? {verify_eds(message, r1_m + 100, s_m)}")
# print()
# print("Четвертый случай: изменена вторая часть подписи")
# print(f"Сообщение: {message}")
# print(f"Подпись: {r1_m} {s_m + 100}")
# print(f"Действительна ли подпись? {verify_eds(message, r1_m, s_m + 100)}")
# print()
# print("Пятый случай: все части подписи изменены")
# print(f"Сообщение: {message}")
# print(f"Подпись: {r1_m + 100} {s_m + 100}")
# print(f"Действительна ли подпись? {verify_eds(message, r1_m + 100, s_m + 100)}")
# print()
# print("Шестой случай: изменено всё")
# print(f"Сообщение: {message}1")
# print(f"Подпись: {r1_m + 100} {s_m + 100}")
# print(f"Действительна ли подпись? {verify_eds(message + "1", r1_m + 100, s_m + 100)}")
# print()
