def print_texts(texts, theme, encryptor, decryptor):
    print(f"===== {theme} =====")
    for i, t in enumerate(texts):
        print(f"=== example {i + 1} ===")
        t_lower = t.lower()
        print(f"Исходный:\t\t\t{t_lower}")
        print(f"Шифрованный:\t\t{(encrypted := encryptor(t_lower))}")
        print(f"Расшифрованный:\t\t{(decrypted := decryptor(encrypted))}")
        print(f"Исходный = расшифрованный?: {t_lower == decrypted.strip()}")
        print()
    print()
