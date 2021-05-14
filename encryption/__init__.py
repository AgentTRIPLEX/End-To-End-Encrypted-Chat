import random
from . import binary

BITS = 4
SEP = "."

def generate_code(bits=BITS):
    uppercase = [chr(l) for l in range(ord("A"), ord("Z")+1)]
    lowercase = [l.lower() for l in uppercase]
    nums = list(map(str, range(10)))
    strings = uppercase + lowercase + nums

    code_len = len(binary.get_possible_bins(bits))
    code = []
    while len(code) < code_len:
        char = random.choice(strings)
        code.append(char)
        strings.remove(char)

    return "".join(code)

def encrypt(data, code, sep=SEP, bits=BITS):
    ints = list(data)
    bins = binary.get_possible_bins(bits)
    key = {bins[i]: code[i] for i in range(len(bins))}
    bins = [binary.split_bin(binary.int_to_bin(i), bits) for i in ints]
    encrypted = [[key[b] for b in a] for a in bins]
    return sep.join(["".join(b) for b in encrypted])

def decrypt(data, code, sep=SEP, bits=BITS):
    if not data:
        return b""

    encrypted = data.split(sep)
    bins = binary.get_possible_bins(bits)
    key = {code[i]: bins[i] for i in range(len(bins))}
    bins = ["".join([key[b] for b in a]) for a in encrypted]
    ints = [binary.bin_to_int(b) for b in bins]
    return bytes(ints)
