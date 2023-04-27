# Bartosz Brodowski

import argparse

def prepare():
    with open("orig.txt", "r", encoding="US-ASCII") as orig, open("plain.txt", "w", encoding="US-ASCII") as plain:
        orig_text = orig.read().lower()
        cleaned_text = "".join(char for char in orig_text if char.isalnum() or char == " ")
        formatted_lines = [cleaned_text[i:i+64] for i in range(0, len(cleaned_text), 64)]
        plain.write("\n".join(formatted_lines))


def xor_pairs(n, m):
    a_ascii = ord(n)
    b_ascii = ord(m)
    return chr(a_ascii ^ b_ascii)

def xor_string(s, c):
    return "".join(xor_pairs(x, c) for x in s)

def find_spaces(text_pairs):
    result = []
    for pair in text_pairs:
        if ' ' in pair:
            result.append(' ')
        else:
            result.append('?')
    return "".join(result)

def clean_decoded_line(line):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789 ")
    cleaned_line = ''.join(char for char in line if char in allowed_chars)
    return cleaned_line

def encrypt():
    with open("plain.txt", "r", encoding="US-ASCII") as plain, open("key.txt", "r", encoding="US-ASCII") as key_file, open("crypto.txt", "w", encoding="US-ASCII") as crypto:
        key = key_file.read().strip()
        new_key = [ord(c) for c in key]
        for line in plain:
            encrypted_line = "".join(chr(ord(c) ^ new_key[i % len(new_key)]) for i, c in enumerate(line.strip()))
            crypto.write(encrypted_line + "\n")

def cryptoanalysis():
    with open("crypto.txt", "r", encoding="US-ASCII") as crypto:
        lines = [line.strip() for line in crypto.readlines()]
        n = len(lines)
        max_len = max(len(line) for line in lines)
        padded_lines = [line.ljust(max_len, '\0') for line in lines]
        pairs_xor = [["".join(xor_pairs(padded_lines[i][j], padded_lines[i + 1][j]) for j in range(len(padded_lines[i]))) for i in range(n - 1)] for _ in range(n)]
        spaces = [find_spaces(pairs) for pairs in pairs_xor]
        possible_texts = [[xor_string(pair, space) for pair, space in zip(pairs, line_spaces)] for pairs, line_spaces in zip(pairs_xor, spaces)]
        with open("decrypt.txt", "w", encoding="US-ASCII") as decrypt:
            for line in possible_texts:
                cleaned_lines = [clean_decoded_line(decoded_line) for decoded_line in line]
                for cleaned_line in cleaned_lines:
                    decrypt.write(cleaned_line + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prepare", action="store_true", help="Prepare the plain text")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the plain text")
    parser.add_argument("-k", "--cryptoanalysis", action="store_true", help="Cryptoanalysis based on encrypted text")
    args = parser.parse_args()

    if args.prepare:
        prepare()
    if args.encrypt:
        encrypt()
    if args.cryptoanalysis:
       cryptoanalysis()

if __name__ == "__main__":
    main()