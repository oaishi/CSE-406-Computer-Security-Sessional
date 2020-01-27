from Mapping import *

deciphered_text = ''
final_deciphered_text = ''
final_ciphered_text = ''

Plaintext = input('Text:')
padding_count = 0

def binary_converter(ascii_value):
    bits = bin(int.from_bytes(ascii_value.encode('ascii'), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def ascii_converter(bytearr):
    return ''.join(chr(int(bytearr[i * 8:i * 8 + 8], 2)) for i in range(len(bytearr) // 8))

def universe_permute(data, map, iter):
    perm = ""
    for iter1 in range(iter):
        temp = map[iter1] - 1
        perm += data[temp]
    return perm

def circular_shift(matrix, iter):
    result = ""
    for iter1 in range(iter):
        for iter2 in range(1, 28):
            result += matrix[iter2]
            result += matrix[0]
        matrix = result
        result = ""
    return matrix

def XOR(first, second):
    result = ""
    for iter in range(len(first)):
        if first[iter] == second[iter]:
            result += "0"
        else:
            result += "1"
    return result

def Encrypt(initial_data, iter):
    initial_data = universe_permute(initial_data, PI, 64)
    left_half = initial_data[0: 32]
    right_half = initial_data[32:]

    for iter1 in range(16):
        right_perm = universe_permute(right_half, E, 48)
        xor_of_right = XOR(iter[iter1], right_perm)
        pi2_result = universe_permute(xor_of_right, PI_2, 32)
        p_result = universe_permute(pi2_result, P, 32)
        xor_result = XOR(p_result, left_half)
        left_half = xor_result
        if (iter1 != 15):
            left_half, right_half = right_half, left_half

    recombined_data = left_half + right_half
    cipher = universe_permute(recombined_data, PI_1, 64)
    ciphered_text = ascii_converter(cipher)
    return [cipher, ciphered_text]



#input padding
if (len(Plaintext) % 8) != 0:
    n = 8 - (len(Plaintext) % 8)
    padding_count = n
    for recur_iter in range(n):
        Plaintext += '.'

print(Plaintext)
input_x = Plaintext
Key_ = input('Key:')

while (len(Key_) != 8):
    Key_ = input('Key:')


for iter in range(int(len(input_x) // 8)):
    periterkey = []
    Plaintext = input_x[iter * 8:iter * 8 + 8]
    Key = Key_
    Key = binary_converter(Key)
    Key = universe_permute(Key, CP_1, 56)
    print("Key:", Key, len(Key))
    left_half = Key[0: 28]
    right_half = Key[28:]

    for recur_iter in range(16):
        right_half = circular_shift(right_half, SHIFT[recur_iter])
        left_half = circular_shift(left_half, SHIFT[recur_iter])
        recombined_data = left_half + right_half
        tempKey = universe_permute(recombined_data, CP_2, 48)
        print("Per iteration Key:", recur_iter, tempKey)
        periterkey.append(tempKey)

    Plaintext = binary_converter(Plaintext)
    cipher_ = Encrypt(Plaintext, periterkey)
    periterkey.reverse()
    final_ciphered_text += cipher_[1]
    cipher = cipher_[0]
    dec_ = Encrypt(cipher, periterkey)
    deciphered_text = dec_[1]
    final_deciphered_text += deciphered_text
    #print("Per iteration text:", recur_iter, deciphered_text)


print("Plaintext:", repr(final_ciphered_text))
print("Decrypted text : %r" % final_deciphered_text)
print("Decrypted Plain text:", final_deciphered_text[:len(final_deciphered_text) - padding_count])

# Ìz/ÈNgu® 8
# Ìz/ÈNgu® 8