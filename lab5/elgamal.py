# Bartosz Brodowski

import random
import sys
import argparse


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


def key_generation():
    with open("elgamal.txt", "r") as f:
        p = int(f.readline().replace("\n", ""))
        g = int(f.readline().replace("\n", ""))
    private_key = random.randint(10**20, p)

    while gcd(p, private_key) != 1:
        private_key = random.randint(10**20, p)
    public_key = pow(g, private_key, p)

    with open("public.txt", "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(public_key))

    with open("private.txt", "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(private_key))

    print("Keys successfully saved in a files.")
    return True


def verify():
    with open("public.txt", "r") as f:
        p = int(f.readline().replace("\n", ""))
        g = int(f.readline().replace("\n", ""))
        public_key = int(f.readline().replace("\n", ""))

    with open("signature.txt", "r") as f:
        r = int(f.readline().replace("\n", ""))
        x = int(f.readline().replace("\n", ""))
        msg = int(f.readline().replace("\n", ""))

    v1 = pow(g, msg, p)
    v2 = pow(r, x, p) % p * pow(public_key, r, p) % p
    print(str(v1) + "\n" + str(v2))

    if v1 == v2:
        with open("verify.txt", "w") as f:
            f.write("True")
        print("Veryfication: True")

    else:
        with open("verify.txt", "w") as f:
            f.write("False")
        print("Veryfication: False")

    return True


def signature():
    with open("message.txt", "r") as f:
        msg = int(f.readline().replace("\n", ""))

    with open("private.txt", "r") as f:
        p = int(f.readline().replace("\n", ""))
        g = int(f.readline().replace("\n", ""))
        b = int(f.readline().replace("\n", ""))

    if not msg < p:
        return False

    while True:
        k = random.randint(1, p - 2)
        if gcd(k, p - 1) == 1:
            break

    r = pow(g, k, p)
    ik = pow(k, -1, p - 1)
    x = ((msg - b * r) * ik) % (p - 1)
    with open("signature.txt", "w") as f:
        f.write(str(r) + "\n")
        f.write(str(x) + "\n")
        f.write(str(msg))
    return True


def encryption():
    with open("public.txt", "r") as f:
        p = int(f.readline().replace("\n", ""))
        g = int(f.readline().replace("\n", ""))
        public_key = int(f.readline().replace("\n", ""))
    k = random.randint(10**20, p)
    while gcd(p, k) != 1:
        k = random.randint(10**20, p)

    with open("plain.txt", "r") as f:
        msg = int(f.readline().replace("\n", " "))

    if not msg < p:
        return False

    with open("crypto.txt", "w") as f:
        f.write(str(pow(g, k, p)) + "\n" + str((pow(public_key, k, p) * msg)))

    return True


def decryption():
    with open("crypto.txt", "r") as f:
        gk = int(f.readline().replace("\n", ""))
        msg = int(f.readline().replace("\n", ""))

    with open("private.txt", "r") as f:
        p = int(f.readline().replace("\n", ""))
        b = int(f.readline().replace("\n", ""))

    key = pow(gk, b, p)
    with open("decrypt.txt", "w") as f:
        f.write(str(int(msg // key)))
    return True


s1 = sys.argv[1]

todo = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keygen", action="store_true")
    parser.add_argument("-e", "--encrypt", action="store_true")
    parser.add_argument("-d", "--decryption", action="store_true")
    parser.add_argument("-s", "--signature", action="store_true")
    parser.add_argument("-v", "--verify", action="store_true")
    args = parser.parse_args()

    if args.keygen:
        key_generation()
    if args.encrypt:
        encryption()
    if args.decryption:
        decryption()
    if args.signature:
        signature()
    if args.verify:
        verify()


if __name__ == "__main__":
    main()
