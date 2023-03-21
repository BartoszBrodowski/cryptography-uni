# Bartosz Brodowski

import sys
import argparse
import math


parser = argparse.ArgumentParser(description='Script to encrypt and decrypt text using Ceasar cipher and Affine cipher')

parser.add_argument('-c', '--ceasar', action='store_true', help='Ceasar cipher')
parser.add_argument('-a', '--affine', action='store_true', help='Affine cipher')
parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt text')
parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt text')

args = parser.parse_args()


# Helper functions

def nwd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# For the inverse of a (multiplier) in affine_cipher

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
                    if key[0].strip() == "":
                        with open('crypto.txt', 'r') as crypto:
                            encrypted_text = crypto.readline()
                            if encrypted_text != "":
                                diff = ord(text[0]) - ord(encrypted_text[0])
                                decrypted.write(ceasar_cipher(text, diff * -1))
                                decrypted.write('\n')
                            else:
                                print('Error: No text to decrypt')
                                sys.exit()
                        for i in range(1, 26):
                            decrypted.write(ceasar_cipher(text, i))
                            decrypted.write('\n')
                    else:
                        decrypted.write(ceasar_cipher(text, int(key[0]) * -1))
                        print('Decrypted text saved to decrypt.txt')

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
                    if key[0] == "":
                        for i in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
                            for j in range(1, 27):
                                decrypted.write(affine_cipher_decrypt(text, i, j))
                                decrypted.write('\n')
                    elif not key[0].isnumeric() or not key[1].isnumeric():
                        print('Error: Key must be an integer')
                        sys.exit()
                    else:
                        decrypted.write(affine_cipher_decrypt(text, int(key[0]), int(key[1])))
                        print('Decrypted text saved to decrypt.txt')
