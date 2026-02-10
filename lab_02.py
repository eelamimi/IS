from utils import print_texts

def get_m():
    return 2 ** b


def generator(t_last):
    return (a * t_last + c) % m


a, c, t_0, b = 5, 3, 7, 7
m = get_m()

texts = ['абв']


def encrypt_linear_gamma(raw):
    encrypted_linear = ""
    t_last = generator(t_0)
    for c in raw:
        encrypted_linear += chr(ord(c) ^ t_last)
        t_last = generator(t_last)
    return encrypted_linear


def decrypt_linear_gamma(encrypted_linear):
    return encrypt_linear_gamma(encrypted_linear)


print_texts(texts, "Линейные конгруэнтные датчики ПСЧ", encrypt_linear_gamma, decrypt_linear_gamma)

b = 8
m = get_m()


def encrypt_gamma_feedback(raw):
    encrypted_feedback = ""
    t_last = generator(t_0)
    for c in raw:
        encrypted_feedback += chr(ord(c) ^ t_last)
        t_last = generator(bin(ord(c))[2:].count("1"))
    return encrypted_feedback


def decrypt_gamma_feedback(encrypted_gamma):
    decrypted_feedback = ""
    t_last = generator(t_0)
    for c in encrypted_gamma:
        xor_res = ord(c) ^ t_last
        decrypted_feedback += chr(xor_res)
        t_last = generator(bin(xor_res)[2:].count("1"))
    return decrypted_feedback


print_texts(texts, "Гаммирование с обратной связью", encrypt_gamma_feedback, decrypt_gamma_feedback)
