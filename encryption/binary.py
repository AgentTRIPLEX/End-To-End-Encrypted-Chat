import re
import itertools

def int_to_bin(denary):
    if denary <= 0:
        return "0"

    table = get_int_table(denary)
    binary = None

    n = 1
    while not binary:
        for combo in itertools.combinations(table, n):
            if sum(combo) == denary:
                binary = ["0" for _ in table]
                for n in combo:
                    binary[table.index(n)] = "1"
                binary = "".join(binary)
                break
        n += 1

    return binary

def split_bin(binary, bits):
    bins = []

    i = 0
    while i < len(binary):
        bins.append([binary[len(binary) - i - 1] for i in range(len(binary))][i:(i + bits)])
        i += bits

    bins = ["".join([b[len(b) - i - 1] for i in range(len(b))]) for b in bins]
    bins = [((("0"*(bits - len(b))) + b) if len(b) < bits else b) for b in bins]
    bins = ["".join(b) for b in bins]
    bins = [bins[len(bins) - i - 1] for i in range(len(bins))]

    return bins

def bin_to_int(binary):
    table = get_bin_table(binary)
    return sum([a for a,b in table.items() if b == "1"])

def get_int_table(denary):
    table = []

    n = 1
    while sum(table) < denary:
        table.append(n)
        n *= 2

    return sorted(table, reverse=True)

def get_bin_table(binary):
    table = {}

    n = 1
    for i in range(len(binary)):
        table[n] = binary[len(binary) - i - 1]
        n *= 2

    return {e:table[e] for e in sorted(table, reverse=True)}

def get_possible_bins(bits):
    bins = []

    n = 0
    while len(split_bin(str(n), bits)) == 1:
        if re.match("[01]{" + str(bits) + "}", split_bin(str(n), bits)[0]):
            bins.append(split_bin(str(n), bits)[0])
        n += 1

    return bins
