# Bartosz Brodowski 2023

import sys

flag = sys.argv[1]

LINE_LENGTH = 64


def encrypt():
    with open("plain.txt", "r") as plain:
        plain = plain.read()

        plain = plain.replace("\n", "8")
        plain = plain.split("8")

        with open("key.txt", "r") as key:
            key = key.read()

            # Dzielenie klucza na elementy 8-bitowe
            key = " ".join(format(ord(i), "b") for i in key)
            key = key.split(" ")
            for i in range(len(key)):
                while len(key[i]) != 8:
                    key[i] = "0" + key[i]
            key = "".join(format(x) for x in key)

            for l in range(len(plain)):
                new_line = ""
                coded_line = ""

                line = " ".join(format(ord(i), "b") for i in plain[l])
                line = line.split(" ")

                for i in range(len(line)):
                    while len(line[i]) != 8:
                        line[i] = "0" + line[i]

                line = "".join(format(x) for x in line)

                if line != "00000000":
                    for i in range(len(line)):
                        result = int(line[i]) ^ int(key[i])
                        if result:
                            coded_line += "1"
                        else:
                            coded_line += "0"
                        new_line = new_line + str(result)
                    with open("crypto.txt", "a") as f:
                        f.write(new_line + "\n")


def prepare_text():
    with open("orig.txt", "r") as orig:
        orig = orig.read()

        orig = orig.lower()
        orig = orig.replace("\n", " ")
        line = ""
        with open("plain.txt", "w") as plain:
            for i, ch in enumerate(orig):
                line += ch
                if (i + 1) % LINE_LENGTH == 0 and i != 0:
                    line += "\n"
                    plain.write(line)
                    line = ""

            if len(line) > 0:
                while len(line) != LINE_LENGTH:
                    line += " "

            line += "\n"
            plain.write(line)


def cryptoanalisis():
    with open("crypto.txt", "r") as crypto:
        crypto = crypto.read()

        crypto = crypto.replace("\n", "*")
        crypto = crypto.split("*")
        crypto.pop(len(crypto) - 1)

        # Wpisywanie zakodowanych linii do pliku crypto.txt
        for index, line in enumerate(crypto):
            # Dzielenie crypto[index] na elementy 8-bitowe
            output = [line[i : i + 8] for i in range(0, len(line), 8)]
            crypto[index] = output

        for row_index, row in enumerate(crypto):
            for column_index, column in enumerate(row):
                reset_char = False
                if len(column) > 1:
                    if column[1] == "1":
                        reset_char = column
                    if reset_char:
                        for i in range(len(crypto)):
                            coded_char = crypto[i][column_index]
                            coded_line = ""

                            for j in range(8):
                                result = int(coded_char[j]) ^ int(reset_char[j])
                                if result:
                                    coded_line += "1"
                                else:
                                    coded_line += "0"
                            if coded_line == "00000000":
                                crypto[i][column_index] = " "
                            else:
                                crypto[i][column_index] = chr(int(coded_line, 2))

    with open("decrypt.txt", "w") as decrypt:
        for row in crypto:
            for column in row:
                decrypt.write(column.lower())
            decrypt.write("\n")


if flag in ["-p", "p"]:
    prepare_text()
    print("Prepare text")
elif flag in ["-e", "e"]:
    encrypt()
    print("Encrypt")
elif flag in ["-k", "k"]:
    cryptoanalisis()
    print("Cryptoanalisis")
else:
    print("Wrong parameter: {}".format(flag))
