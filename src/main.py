from binascii import hexlify, unhexlify
import translation

initial_permutation_table = [58, 50, 42, 34, 26, 18, 10, 2,
                             60, 52, 44, 36, 28, 20, 12, 4,
                             62, 54, 46, 38, 30, 22, 14, 6,
                             64, 56, 48, 40, 32, 24, 16, 8,
                             57, 49, 41, 33, 25, 17, 9, 1,
                             59, 51, 43, 35, 27, 19, 11, 3,
                             61, 53, 45, 37, 29, 21, 13, 5,
                             63, 55, 47, 39, 31, 23, 15, 7]

final_permutation_table = [ 40, 8, 48, 16, 56, 24, 64, 32,
                            39, 7, 47, 15, 55, 23, 63, 31,
                            38, 6, 46, 14, 54, 22, 62, 30,
                            37, 5, 45, 13, 53, 21, 61, 29,
                            36, 4, 44, 12, 52, 20, 60, 28,
                            35, 3, 43, 11, 51, 19, 59, 27,
                            34, 2, 42, 10, 50, 18, 58, 26,
                            33, 1, 41, 9, 49, 17, 57, 25]

expansion_table = [32, 1, 2, 3, 4, 5, 4, 5,
                   6, 7, 8, 9, 8, 9, 10, 11,
                   12, 13, 12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21, 20, 21,
                   22, 23, 24, 25, 24, 25, 26, 27,
                   28, 29, 28, 29, 30, 31, 32, 1]

        # S1
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Number of bit shifts
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

p_box = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

key_parity_table = [57, 49, 41, 33, 25, 17, 9,
                    1, 58, 50, 42, 34, 26, 18,
                    10, 2, 59, 51, 43, 35, 27,
                    19, 11, 3, 60, 52, 44, 36,
                    63, 55, 47, 39, 31, 23, 15,
                    7, 62, 54, 46, 38, 30, 22,
                    14, 6, 61, 53, 45, 37, 29,
                    21, 13, 5, 28, 20, 12, 4]

# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_compression_table = [14, 17, 11, 24, 1, 5,
                         3, 28, 15, 6, 21, 10,
                         23, 19, 12, 4, 26, 8,
                         16, 7, 27, 20, 13, 2,
                         41, 52, 31, 37, 47, 55,
                         30, 40, 51, 45, 33, 48,
                         44, 49, 39, 56, 34, 53,
                         46, 42, 50, 36, 29, 32]


def main():
    #e = "abcghijk".encode()
    #e = "123456abcd132536".encode()
    #m = hexlify(e).decode()
    m = "123456abcd132536"
    message = translation.hex2bin(m)

    key64 = translation.hex2bin("aabb09182736ccdd")
    key56 = key_permutation(key64)

    round_keys48 = []
    for i in range(0, 16):
        key56 = key_round(key56, i)
        round_keys48.append(compression(key56))

    # for i in range(0, 16):
    #     message = des_round(message, round_keys48[i])
    # print("")
    # rev_message = message
    # for i in range(15, -1, -1):
    #     rev_message = des_round(rev_message, round_keys48[i])

    cipher_text = encrypt(message, round_keys48)
    print("Encrypted:", translation.bin2hex(cipher_text))

    #decrypted = decrypt(cipher_text, round_keys48)
   # print("Decrypted:", translation.bin2hex(decrypted))
    # if message == decrypted:
    #     print("Dziala")
    # else:
    #     print("Nie dziala")
    #decrypted = unhexlify(decrypted.encode())
    #print("Decryptded:\n", decrypted.decode())


def encrypt(message, round_keys48):  # 48 bits keys
    print("Encryption:")
    cipher_text = message
    cipher_text = initial_permutation(cipher_text)
    print("Initial: {ciph}".format(ciph=translation.bin2hex(cipher_text)))
    for i in range(0, 16):
        cipher_text = des_round(cipher_text, round_keys48[i], i)

    cipher_text = final_permutation(cipher_text)
    return cipher_text


def decrypt(message, round_keys48):
    print("Decryption:")
    cipher_text = message
    cipher_text = initial_permutation(cipher_text)
    print("Initial: {ciph}".format(ciph=translation.bin2hex(cipher_text)))
    for i in range(15, -1, -1):
        cipher_text = des_round(cipher_text, round_keys48[i])

    cipher_text = final_permutation(cipher_text)
    #print("Final:   {ciph}".format(ciph=translation.bin2hex(cipher_text)))
    return cipher_text


def initial_permutation(input_) -> str:
    result = ""
    for i in range(0, 64):
        result = result + input_[initial_permutation_table[i] - 1]
    return result


def final_permutation(input_) -> str:
    result = ""
    for i in range(0, 64):
        result = result + input_[final_permutation_table[i] - 1]
    return result


def des_round(block, key, i):
    l = block[0:32]
    r = block[32:64]
    l_prim = r
    r = expansion(r)  # expansion to 48
    r = xor(r, key)
    r = sbox_permutation(r)  # sboxes compress to 32 bits
    r = p_box_permutation(r)
    r_prim = xor(l, r)
    if i != 15:
        cipher_text = l_prim + r_prim
    else:
        cipher_text = r_prim + l_prim
    return cipher_text


def expansion(input_) -> str:
    result = ""
    for i in range(0, 48):
        result = result + input_[expansion_table[i] - 1]
    return result


def sbox_permutation(input_):
    result = ""
    for i in range(0, 8):
        s_row = translation.bin2dec(int(input_[i * 6] + input_[i * 6 + 5]))
        s_col = translation.bin2dec(int(input_[i * 6 + 1] + input_[i * 6 + 2] + input_[i * 6 + 3] + input_[i * 6 + 4]))
        # s_row = int(input_[0] + input_[5], 2)
        # s_col = int(input_[1:5], 2)
        result = result + translation.dec2bin(sbox[i][s_row][s_col])
    return result


def p_box_permutation(input_) -> str:
    result = ""
    for i in range(0, 32):
        result = result + input_[p_box[i] - 1]
    return result


def xor(a, b) -> str:
    result = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            result = result + "0"
        else:
            result = result + "1"
    return result


def key_permutation(key_hex) -> str:
    result = ""
    for i in range(0, 56):
        result = result + key_hex[key_parity_table[i] - 1]
    return result


def key_round(key, i) -> str:
    l = key[0:28]
    r = key[28:56]
    for j in range(0, shift_table[i]):
        l = rotation(l)
        r = rotation(r)
    return l + r


def rotation(half_key) -> str:
    first = half_key[0]
    half_key = half_key[1:]
    return half_key + first


def compression(key) -> str:
    result = ""
    for i in range(0, 48):
        result = result + key[key_compression_table[i] - 1]
    return result



if __name__ == "__main__":
    main()
