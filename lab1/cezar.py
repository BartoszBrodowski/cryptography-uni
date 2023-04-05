# Bartosz Brodowski

import sys
import argparse

parser = argparse.ArgumentParser(description='Script to encrypt and decrypt text using Ceasar cipher and Affine cipher')

parser.add_argument('-c', '--ceasar', action='store_true', help='Ceasar cipher')
parser.add_argument('-a', '--affine', action='store_true', help='Affine cipher')
parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt text')
parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt text')
parser.add_argument('-j', '--cryptoplain', action='store_true', help='Cryptoanalisis with plain text')
parser.add_argument('-k', '--cryptonoplain', action='store_true', help='Cryptoanalisis without plain text')

args = parser.parse_args()


# Helper functions

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def ceasar_cipher(text,shift_number):
    result = ""
    for character in text:
        if not character.isalpha():
            result += character
        elif (character.isupper()):
            result += chr((ord(character) + shift_number-65) % 26 + 65)
        else:
            result += chr((ord(character) + shift_number-97) % 26 + 97)
    return result

def affine_cipher(text, a=None, b=None):
    if a is None or b is None:
        pass
    else:
        if a < 1 or a > 25:
            print('Error: a must be between 1 and 26')
            sys.exit()
        if b < 0 or b > 25:
            print('Error: Shift number must be between 0 and 26')
            sys.exit()
    result = ""
    for character in text:
        if not character.isalpha():
            result += character
        elif (character.isupper()):
            humanized_number = ord(character) - 65
            formula = (humanized_number * a + b) % 26
            result += chr(formula + 65)
        else:
            humanized_number = ord(character) - 97
            formula = (humanized_number * a + b) % 26
            result += chr(formula + 97)
    return result
    
def affine_cipher_decrypt(cipher_text, a, b):
    plain_text = ""
    a_inv = pow(a, -1, 26)
    for character in cipher_text:
        if character.isalpha():
            num = ord(character) - 65
            num = a_inv * (num - b) % 26
            character = chr(num + 65)
        plain_text += character
    return plain_text

if args.ceasar:
    if args.encrypt:
        print('Ceasar cipher')

        with open('plain.txt') as plain:
            text = plain.readline()

            with open('crypto.txt', 'w') as encrypted:
                with open('key.txt') as key:
                    key = key.readline()
                    key = key.strip().split(' ')
                    if not key[0].isnumeric():
                        print('Error: Key must be an integer')
                        sys.exit()
                if int(key[0]) < 1 or int(key[0]) > 25:
                    print('Error: Shift number must be between 1 and 26')
                    sys.exit()
                encrypted.write(ceasar_cipher(text, int(key[0])))
                print('Encrypted text saved to crypto.txt')

    elif args.decrypt:
        print('Ceasar cipher')
        with open('crypto.txt') as f:
            text = f.readline()
            with open('decrypt.txt', 'w') as decrypted:
                with open('key.txt') as key:
                    key = key.readline()
                    key = key.strip().split(' ') 
                    if key[0] == "":
                        print("Key not provided")
                        sys.exit()
                    if not key[0].isnumeric():
                        print('Error: Key must be an integer')
                        sys.exit()
                    decrypted.write(ceasar_cipher(text, int(key[0]) * -1))
                    print('Decrypted text saved to decrypt.txt')

    elif args.cryptoplain:
        print("Ceasar cipher")
        with open('crypto.txt') as encrypted:
            with open('extra.txt') as extra:
                encrypted_text = encrypted.readline().strip()
                extra_text = extra.readline().strip()
                for key in range(26):
                    decrypted_text = ceasar_cipher(encrypted_text, key * -1)
                    if decrypted_text.startswith(extra_text):
                        with open('key-found.txt', 'w') as key_found:
                            key_found.write(str(key))
                            with open('decrypt.txt', 'w') as decrypted:
                                decrypted.write(decrypted_text)
                                break

    elif args.cryptonoplain:
        print('Ceasar cipher')
        with open('crypto.txt') as f:
            text = f.readline()
            with open('decrypt.txt', 'w') as decrypted:
                for i in range(1, 26):
                    decrypted.write(ceasar_cipher(text, i))
                    decrypted.write('\n')

if args.affine:
    if args.encrypt:
        print('Affine cipher')
        
        with open('plain.txt') as plain:
                text = plain.readline()

                with open('crypto.txt', 'w') as encrypted:
                    with open('key.txt') as key:
                        key = key.readline()
                        key = key.strip().split(' ')
                        if not key[0].isnumeric() or not key[1].isnumeric():
                            print('Error: Key must be an integer')
                            sys.exit()
                    encrypted.write(affine_cipher(text, int(key[0]), int(key[1])))
                    print('Encrypted text saved to crypto.txt')
    if args.decrypt:
        print("Affine cipher")

        with open('crypto.txt') as f:
            text = f.readline()

            with open('decrypt.txt', 'w') as decrypted:
                with open('key.txt') as key:
                    key = key.readline()
                    key = key.strip().split(' ')
                    if not key[0].isnumeric() or not key[1].isnumeric():
                        print('Error: Key must be an integer')
                        sys.exit()
                    else:
                        decrypted.write(affine_cipher_decrypt(text, int(key[0]), int(key[1])))
                        print('Decrypted text saved to decrypt.txt')

    if args.cryptoplain:
        print("Affine cipher")
        with open('crypto.txt', 'r') as encrypted:
            with open('extra.txt') as extra:
                extra_text = extra.readline().strip()
                encrypted_text = encrypted.read().strip()
                found = False
                for a in range(1, 27):
                    if gcd(a, 26) != 1:
                        continue
                    for b in range(26):
                        decrypted_text = affine_cipher_decrypt(encrypted_text, a, b)
                        if decrypted_text.startswith(extra_text):
                            with open('key-found.txt', 'w') as key_found:
                                key_found.write(f'{a} {b}')
                                with open('decrypt.txt', 'w') as decrypted:
                                    decrypted.write(decrypted_text)
                                    found = True
                                    break
                    if found:
                        break

    if args.cryptonoplain:
        print("Affine cipher")
        with open('crypto.txt') as f:
            text = f.readline()
            with open('decrypt.txt', 'w') as decrypted:
                for i in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
                    for j in range(1, 27):
                        decrypted.write(affine_cipher_decrypt(text, i, j))
                        decrypted.write('\n')

