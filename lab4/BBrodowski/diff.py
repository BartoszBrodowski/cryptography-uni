# Bartosz Brodowski

import hashlib


def compare_hashes(file1, file2):
    hash_functions = [
        ("md5", hashlib.md5),
        ("sha1", hashlib.sha1),
        ("sha224", hashlib.sha224),
        ("sha256", hashlib.sha256),
        ("sha384", hashlib.sha384),
        ("sha512", hashlib.sha512),
        ("b2sum", hashlib.blake2b),
    ]

    results = []
    for name, hash_func in hash_functions:
        hash1 = hash_func()
        hash2 = hash_func()

        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            hash1.update(f1.read())
            hash2.update(f2.read())

        result = (hash1.hexdigest(), hash2.hexdigest())
        results.append((name, result))

    return results


def count_different_bits(hash_pairs):
    diff_counts = []
    for name, (hash1, hash2) in hash_pairs:
        count = sum(
            bin(int(a, 16) ^ int(b, 16)).count("1") for a, b in zip(hash1, hash2)
        )
        diff_counts.append((name, count))
    return diff_counts


def count_bits_difference(hash1, hash2):
    different_bits_amount = 0
    for char in range(len(hash1)):
        binary_value1 = bin(int(hash1[char], 16))[2:].zfill(4)
        binary_value2 = bin(int(hash2[char], 16))[2:].zfill(4)
        for i in range(4):
            if binary_value1[i] == binary_value2[i]:
                different_bits_amount += 1

    return different_bits_amount


def write_results_to_file(results, hash_pairs):
    with open("diff.txt", "w") as f:
        for i in range(len(hash_pairs)):
            f.write(f"{results[i][0]}:\n")
            f.write(f"{hash_pairs[i][1][0]}\n")
            f.write(f"{hash_pairs[i][1][1]}\n")
            bits_difference = count_bits_difference(
                hash_pairs[i][1][0], hash_pairs[i][1][1]
            )
            f.write(
                f"Liczba rozniacych sie bitow: {bits_difference} z {len(hash_pairs[i][1][0]) * 4}, procentowo {str(100 - round(len(hash_pairs[i][1][0]) / bits_difference * 100, 0))[:-2]}%\n\n"
            )


file1 = "personal.txt"
file2 = "personal_.txt"
hash_pairs = compare_hashes(file1, file2)
diff_counts = count_different_bits(hash_pairs)

write_results_to_file(diff_counts, hash_pairs)
