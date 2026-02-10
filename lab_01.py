from utils import print_texts

eng_alphabet = "".join(sorted("qwertyuiopasdfghjklzxcvbnm")) + " .,!:;?-"
alphabets = [
    'cdabhijefgopqrklmnuvw:stz xy;?-.,!',
    'vwxyz .,!:;?-klmnopqrstuabcdefghij'
]
pods_alphabet = 'vwxyz .,!:;?-klmnopqrstuabcdefghij'
k = 3

texts = ["abc", "the. quick brown? fox: jumps, over; the lazy dog!", "the quick brown fox jumps over the lazy dog"]


def encrypt_podstanovka(raw):
    encrypted_pods = ""
    for c in raw:
        encrypted_pods += pods_alphabet[(eng_alphabet.index(c) + k) % len(eng_alphabet)]
    return encrypted_pods


def decrypt_podstanovka(encrypter_pods):
    decrypted_pods = ""
    for c in encrypter_pods:
        decrypted_pods += eng_alphabet[(pods_alphabet.index(c) + len(eng_alphabet) - k) % len(eng_alphabet)]
    return decrypted_pods


print_texts(texts, "Подстановка", encrypt_podstanovka, decrypt_podstanovka)


def encrypt_many(raw):
    encrypted_many = ""
    r = len(alphabets)
    for i, c in enumerate(raw):
        encrypted_many += alphabets[i % r][eng_alphabet.index(c)]
    return encrypted_many


def decrypt_many(encrypted_many):
    decrypted = ""
    r = len(alphabets)
    for i, c in enumerate(encrypted_many):
        decrypted += eng_alphabet[alphabets[i % r].index(c)]
    return decrypted


print_texts(texts, "Многоалфавитный шифр", encrypt_many, decrypt_many)


def encrypt_peres(raw):
    encrypted_peres = ""
    while len(raw) % 6 != 0:
        raw += " "
    for i in range(0, len(raw), 6):
        encrypted_peres += (raw[1 + i] + raw[4 + i] +
                            raw[2 + i] + raw[3 + i] +
                            raw[0 + i] + raw[5 + i])  # 0 1 2 3 4 5
    return encrypted_peres


def decrypt_peres(encrypted_peres):
    decrypted_peres = ""
    for i in range(0, len(encrypted_peres), 6):
        decrypted_peres += (encrypted_peres[4 + i] + encrypted_peres[0 + i] +
                            encrypted_peres[2 + i] + encrypted_peres[3 + i] +
                            encrypted_peres[1 + i] + encrypted_peres[5 + i])
    return decrypted_peres


print_texts(texts, "Метод перестановки", encrypt_peres, decrypt_peres)
