import random


def insert_stego(path: str, message: str) -> str:
    parts = path[::-1].split('.', 1)[::-1]
    new_path = "{0}_with_stego_message.{1}".format(parts[0][::-1], parts[1][::-1])

    message_bytes = message.encode('utf-8')
    message_bytes += b'\x00\x00\x00\x00\x00\x00\x00\x00'
    message_bits = ''.join(f"{byte:08b}" for byte in message_bytes)
    n = len(message_bits)

    with open(path, "rb") as f:
        header = f.read(54)
        pxl = bytearray(f.read())

    if n > len(pxl):
        raise Exception("Not enough data")

    for i in range(n):
        byte = pxl[i]
        lsb = byte & 1
        bit = int(message_bits[i])

        if lsb != bit:
            if random.choice([True, False]):
                if byte < 255:
                    pxl[i] = byte + 1
                else:
                    pxl[i] = byte - 1
            else:
                if byte > 0:
                    pxl[i] = byte - 1
                else:
                    pxl[i] = byte + 1

    data = header + bytes(pxl)
    with open(new_path, "wb") as f:
        f.write(data)

    return new_path


def extract_stego(path: str) -> str:
    with open(path, "rb") as f:
        f.read(54)
        pxl = bytearray(f.read())

    bits = []
    for byte in pxl:
        bits.append(str(byte & 1))
        if len(bits) >= 64 and len(bits) % 8 == 0:
            last_bytes = ''.join(bits[-64:])
            if all(b == '0' for b in last_bytes):
                bits = bits[:-64]
                break

    message_bytes = bytearray()
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) == 8:
            message_bytes.append(int(''.join(byte_bits), 2))
    try:
        return message_bytes.decode('utf-8').rstrip('\x00')
    except:
        return message_bytes.hex()


msg = "Hello world"
print(p := insert_stego("steganography.bmp", msg))
print(extract_stego(p))
