import hashlib
import os


def generate_salt():
    return os.urandom(32).hex().upper()


# 示例：手动计算 SRP6 的 verifier
def calculate_verifier(username, password, salt):
    sha = hashlib.sha1()
    sha.update(f"{username}:{password}".encode())
    x = sha.digest()

    sha = hashlib.sha1()
    sha.update(str2bytes(salt)[::-1])
    sha.update(x)
    x2 = sha.digest()[::-1]

    # 计算 v = g^x mod N
    g = 7  # 常用生成元
    N = int("894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7", 16)
    v = pow(g, int.from_bytes(x2, byteorder="big"), N)

    return int2bytes(v).hex().upper()


def str2bytes(s, order="big", length=None):
    value = int(s, 16)
    if value == 0:
        return b'\x00'
    byte_length = (value.bit_length() + 7) // 8
    if length is not None and length >= byte_length:
        byte_length = length
    return value.to_bytes(byte_length, byteorder=order)


def int2bytes(v, order="big", length=None):
    value = v
    if value == 0:
        return b'\x00'
    byte_length = (value.bit_length() + 7) // 8
    if length is not None and length >= byte_length:
        byte_length = length

    return value.to_bytes(byte_length, byteorder=order)


if __name__ == "__main__":
    user = "1"
    pswd = "1"
    # salt="93257C7EA747E0B6FA4E5A55ECB24869B1161EBBEA6CA84E18BA63BD33B48DB7"
    salt = generate_salt()
    print("salt:", salt)
    v = calculate_verifier(user, pswd, salt)
    print("veri:", v)
