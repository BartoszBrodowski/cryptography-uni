import sys
import argparse

parser = argparse.ArgumentParser(description='Script to encrypt and decrypt text using Ceasar cipher and Affine cipher')

parser.add_argument('-c', '--ceasar', action='store_true', help='Ceasar cipher')
parser.add_argument('-a', '--affine', action='store_true', help='Affine cipher')
parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt text')
parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt text')

args = parser.parse_args()

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

def affine_cipher(text, shift_number, multiplier):
    result = ""
    for character in text:
        if not character.isalpha():
            result += character
        elif (character.isupper()):
            result += chr((multiplier * ord(character) + shift_number-65) % 26 + 65)
        else:
            result += chr((multiplier * ord(character) + shift_number-65) % 26 + 97)
    return result
    

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
