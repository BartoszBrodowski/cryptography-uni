import hashlib

def compare_hashes(file1, file2):
    hash_functions = [
        ('md5', hashlib.md5),
        ('sha1', hashlib.sha1),
        ('sha224', hashlib.sha224),
        ('sha256', hashlib.sha256),
        ('sha384', hashlib.sha384),
        ('sha512', hashlib.sha512),
        ('b2sum', hashlib.blake2b)
    ]

    results = []
    for name, hash_func in hash_functions:
        hash1 = hash_func()
        hash2 = hash_func()

        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            hash1.update(f1.read())
            hash2.update(f2.read())

        result = (hash1.hexdigest(), hash2.hexdigest())
        results.append((name, result))

    return results

def count_different_bits(hash_pairs):
    diff_counts = []
    for name, (hash1, hash2) in hash_pairs:
        count = sum(bin(int(a, 16) ^ int(b, 16)).count('1') for a, b in zip(hash1, hash2))
        diff_counts.append((name, count))
    return diff_counts

def write_results_to_file(results, hash_pairs):
    with open('diff.txt', 'w') as f:
        for i in range(len(hash_pairs)):
            f.write(f'{results[i][0]}:\n')
            f.write(f'{hash_pairs[i][1][0]}\n')
            f.write(f'{hash_pairs[i][1][1]}\n')
            f.write(f'{results[i][1]} bit(s) different\n\n')
            f.write(f'{results[i][1] / len(hash_pairs[i][1][0]) * 100}% different\n\n')

file1 = 'personal.txt'
file2 = 'personal_.txt'
hash_pairs = compare_hashes(file1, file2)
diff_counts = count_different_bits(hash_pairs)

write_results_to_file(diff_counts, hash_pairs)
