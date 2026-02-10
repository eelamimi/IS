import struct
from typing import Tuple, List


class FeistelCipher:
    def __init__(self, key: bytes, rounds: int = 12):
        """
        Инициализация шифра Фейстеля.

        Args:
            key: Ключ в виде байтов (рекомендуется 16-32 байта)
            rounds: Количество раундов (по умолчанию 12)
        """
        self.rounds = rounds
        self.keys = self._key_schedule(key)

    def _key_schedule(self, key: bytes) -> List[bytes]:
        """
        Генерация раундовых ключей из основного ключа.

        Args:
            key: Исходный ключ

        Returns:
            Список раундовых ключей
        """
        # Убедимся, что ключ достаточной длины
        if len(key) < 8:
            key = key.ljust(8, b'\x00')

        # Создаем раундовые ключи (простой метод - можно усложнить)
        keys = []
        for i in range(self.rounds):
            # Используем циклический сдвиг ключа для генерации каждого раундового ключа
            shift = i % len(key)
            round_key = key[shift:] + key[:shift]
            # Берем первые 4 байта как раундовый ключ
            keys.append(round_key[:4])

        return keys

    def _round_function(self, data: bytes, round_key: bytes) -> bytes:
        """
        Раундовая функция: циклический сдвиг вправо + XOR с ключом.

        Args:
            data: Входные данные (4 байта)
            round_key: Ключ раунда (4 байта)

        Returns:
            Результат раундовой функции (4 байта)
        """
        # Преобразуем байты в целое число
        data_int = int.from_bytes(data, byteorder='big')
        key_int = int.from_bytes(round_key, byteorder='big')

        # Циклический сдвиг вправо на 3 позиции
        # (можно изменить количество позиций для настройки)
        bits = 32  # 4 байта = 32 бита
        shift_amount = 3

        # Циклический сдвиг вправо
        right_shifted = data_int >> shift_amount
        wrapped_bits = (data_int & ((1 << shift_amount) - 1)) << (bits - shift_amount)
        rotated = right_shifted | wrapped_bits

        # XOR с ключом раунда
        result = rotated ^ key_int

        # Возвращаем как байты
        return result.to_bytes(4, byteorder='big')

    def _split_block(self, block: bytes) -> Tuple[bytes, bytes]:
        """
        Разделение блока на две равные части.

        Args:
            block: Блок данных (8 байт)

        Returns:
            Кортеж (левая_часть, правая_часть)
        """
        half = len(block) // 2
        return block[:half], block[half:]

    def _merge_block(self, left: bytes, right: bytes) -> bytes:
        """
        Объединение двух половин в один блок.

        Args:
            left: Левая часть
            right: Правая часть

        Returns:
            Объединенный блок
        """
        return left + right

    def encrypt_block(self, block: bytes) -> bytes:
        """
        Шифрование одного блока.

        Args:
            block: Блок для шифрования (8 байт)

        Returns:
            Зашифрованный блок (8 байт)
        """
        # Дополняем блок если необходимо
        if len(block) < 8:
            block = block.ljust(8, b'\x00')
        elif len(block) > 8:
            block = block[:8]

        # Разделяем блок на две части
        left, right = self._split_block(block)

        # Выполняем все раунды
        for i in range(self.rounds):
            # Сохраняем правую часть для следующего раунда
            temp_right = right

            # Применяем раундовую функцию к правой части
            f_result = self._round_function(right, self.keys[i])

            # Преобразуем байты в целые числа для XOR
            left_int = int.from_bytes(left, byteorder='big')
            f_result_int = int.from_bytes(f_result, byteorder='big')

            # XOR левой части с результатом функции F
            new_right = left_int ^ f_result_int
            right = new_right.to_bytes(4, byteorder='big')

            # Левая часть становится предыдущей правой частью
            left = temp_right

        # В последнем раунде не меняем части местами
        # (или можно поменять в зависимости от реализации)
        return self._merge_block(left, right)

    def decrypt_block(self, block: bytes) -> bytes:
        """
        Дешифрование одного блока.

        Args:
            block: Зашифрованный блок (8 байт)

        Returns:
            Расшифрованный блок (8 байт)
        """
        # Разделяем блок на две части
        left, right = self._split_block(block)

        # Выполняем все раунды в обратном порядке
        for i in range(self.rounds - 1, -1, -1):
            # Сохраняем левую часть для следующего раунда
            temp_left = left

            # Применяем раундовую функцию к левой части
            f_result = self._round_function(left, self.keys[i])

            # Преобразуем байты в целые числа для XOR
            right_int = int.from_bytes(right, byteorder='big')
            f_result_int = int.from_bytes(f_result, byteorder='big')

            # XOR правой части с результатом функции F
            new_left = right_int ^ f_result_int
            left = new_left.to_bytes(4, byteorder='big')

            # Правая часть становится предыдущей левой частью
            right = temp_left

        return self._merge_block(left, right)

    def encrypt(self, data: bytes) -> bytes:
        """
        Шифрование произвольных данных.

        Args:
            data: Данные для шифрования

        Returns:
            Зашифрованные данные
        """
        # Дополняем данные до размера, кратного 8 байтам
        padding_length = 8 - (len(data) % 8) if len(data) % 8 != 0 else 0
        data = data + bytes([padding_length] * padding_length)

        # Шифруем по блокам
        encrypted_blocks = []
        for i in range(0, len(data), 8):
            block = data[i:i + 8]
            encrypted_block = self.encrypt_block(block)
            encrypted_blocks.append(encrypted_block)

        return b''.join(encrypted_blocks)

    def decrypt(self, data: bytes) -> bytes:
        """
        Дешифрование данных.

        Args:
            data: Зашифрованные данные

        Returns:
            Расшифрованные данные
        """
        # Дешифруем по блокам
        decrypted_blocks = []
        for i in range(0, len(data), 8):
            block = data[i:i + 8]
            decrypted_block = self.decrypt_block(block)
            decrypted_blocks.append(decrypted_block)

        # Убираем дополнение
        decrypted_data = b''.join(decrypted_blocks)
        padding_length = decrypted_data[-1]

        # Проверяем корректность дополнения
        if padding_length > 0 and padding_length <= 8:
            if decrypted_data[-padding_length:] == bytes([padding_length] * padding_length):
                return decrypted_data[:-padding_length]

        return decrypted_data


# Демонстрация работы шифра
def demo():
    print("=" * 50)
    print("Демонстрация сети Фейстеля с 12 раундами")
    print("Раундовая функция: циклический сдвиг вправо на 3 бита")
    print("=" * 50)

    # Исходные данные
    key = b"MySecretKey123456"  # 16-байтовый ключ
    plaintext = b"Hello, World! This is a test message for Feistel cipher."

    print(f"Ключ: {key}")
    print(f"Исходный текст: {plaintext}")
    print(f"Длина текста: {len(plaintext)} байт")
    print()

    # Создаем шифр
    cipher = FeistelCipher(key, rounds=12)

    # Шифруем
    encrypted = cipher.encrypt(plaintext)
    print(f"Зашифрованный текст (hex): {encrypted.hex()}")
    print(f"Длина зашифрованного текста: {len(encrypted)} байт")
    print()

    # Дешифруем
    decrypted = cipher.decrypt(encrypted)
    print(f"Расшифрованный текст: {decrypted}")
    print()

    # Проверка
    if plaintext == decrypted:
        print("✓ Шифрование/дешифрование прошло успешно!")
    else:
        print("✗ Ошибка в шифровании/дешифровании")

    print()

    # Демонстрация работы с отдельными блоками
    print("Работа с отдельными блоками (8 байт):")
    print("-" * 30)

    test_block = b"ABCDEFGH"  # Ровно 8 байт
    print(f"Тестовый блок: {test_block}")

    encrypted_block = cipher.encrypt_block(test_block)
    print(f"Зашифрованный блок: {encrypted_block.hex()}")

    decrypted_block = cipher.decrypt_block(encrypted_block)
    print(f"Расшифрованный блок: {decrypted_block}")

    if test_block == decrypted_block:
        print("✓ Блок успешно зашифрован и расшифрован!")
    else:
        print("✗ Ошибка с блоком")


if __name__ == "__main__":
    demo()