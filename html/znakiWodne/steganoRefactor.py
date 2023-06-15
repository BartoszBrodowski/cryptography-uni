# Bartosz Brodowski 278830

import re
import sys


def hide_message_algorithm1(cover, message):
    # Sprawdzenie, czy nośnik jest wystarczająco duży dla całej wiadomości
    if cover.count("\n") < 16:
        print(
            "Error: Za mało wierszy w nośniku żeby zaszyfrować wiadomość 64 bitową. Musi być 16 wierszy."
        )
        sys.exit(1)

    lines = cover.split("\n")
    watermark_lines = []
    for i, line in enumerate(lines):
        if i < len(message):
            line += " " * int(message[i], 16)
        watermark_lines.append(line)
    watermark = "\n".join(watermark_lines)

    return watermark


def hide_message_algorithm2(cover, message):
    # Zliczenie unikalnych spacji w nośniku
    space_count = cover.count(" ") - cover.count("    ") * 4
    print(space_count)
    # Ukrywana wiadomość może być co najwyżej długości równej liczbie spacji bez powtórzeń w nośniku.
    if space_count < 64:
        print("Error: Not enough spaces in the cover for the entire message.")
        sys.exit(1)

    messageBinary = bin(int(message, 16))[2:]
    print(messageBinary)
    # zakodowanie wiadomości w postaci bitowej - 0 dla pojedynczej spacji, 1 dla podwójnej
    watermark = cover.split("\n")
    print(watermark)
    for i, line in enumerate(watermark):
        print("LINIA")
        for index, char in enumerate(line):
            print(watermark[i][index])
            if len(messageBinary) == 0:
                break
            elif (
                watermark[i][index] == " "
                and index + 1 < len(line)
                and not (
                    watermark[i][index + 1] == " " or watermark[i][index - 1] == " "
                )
            ):
                print(line)
                print(
                    "to nie jest tabulator, wchodze w spacje pomiędzy literami -"
                    + watermark[i][line.index(char) - 1]
                    + "- i -"
                    + watermark[i][line.index(char) + 1]
                    + "-"
                )

                if messageBinary[0] == "1":
                    print("Podwajam spacje")
                    watermark[i] = (
                        watermark[i][:index] + "  " + watermark[i][index + 1 :]
                    )
                    print("zamienilem na podwojna")
                messageBinary = messageBinary[1:]
    watermark = "\n".join(watermark)
    print(messageBinary)
    return watermark


def hide_message_algorithm3(cover, message):
    # Sprawdzenie, czy nośnik zawiera wystarczającą liczbę znaczników akapitu
    paragraph_tags = re.findall(r"<p.*?>", cover)
    if len(paragraph_tags) < len(message):
        print("Error: Not enough paragraph tags in the cover for the entire message.")
        sys.exit(1)

    # Zamiana prawidłowych nazw atrybutów w znacznikach akapitu na nieprawidłowe nazwy
    watermark = cover
    for i, tag in enumerate(paragraph_tags):
        if i < len(message):
            watermark = watermark.replace(
                tag,
                tag.replace("margin-bottom", "margin-botom").replace(
                    "line-height", "lineheight"
                ),
                1,
            )

    return watermark


def hide_message_algorithm4(cover, message):
    # Znalezienie wystąpień znacznika FONT w nośniku
    font_tags = re.findall(r"<font.*?>", cover)
    if len(font_tags) < len(message):
        print("Error: Not enough FONT tags in the cover for the entire message.")
        sys.exit(1)

    # Zamiana otwarć znacznika FONT na sekwencje otwarcie-zamknięcie-otwarcie w zależności od bitów wiadomości
    watermark = cover
    for i, tag in enumerate(font_tags):
        if i < len(message):
            if int(message[i]) == 1:
                watermark = watermark.replace(tag, tag + "</font>" + tag, 1)
            else:
                watermark = watermark.replace(tag, tag + "</font><font>", 1)

    return watermark


def extract_message_algorithm1(watermark):
    lines = watermark.split("\n")
    # zakładam że wiadomość jest zawsze na początku i jest 64 bitowa
    lines = lines[:16]
    message = ""
    for line in lines:
        spaces_count = len(line) - len(line.rstrip())
        message += hex(spaces_count)[-1]
    return message


def extract_message_algorithm2(watermark):
    # Wyodrębnienie bitów wiadomości z pojedynczych lub podwójnych spacji
    unique_spaces = list(set(re.findall(" +", watermark)))
    message = []
    for space in unique_spaces:
        if len(space) == 1:
            message.append("0")
        elif len(space) == 2:
            message.append("1")

    return "".join(message)


def extract_message_algorithm3(watermark):
    # Wyodrębnienie bitów wiadomości z nieprawidłowych nazw atrybutów w znacznikach akapitu
    matches = re.findall(r'<p style="(.*?)">', watermark)
    message = []
    for match in matches:
        if "margin-botom" in match or "lineheight" in match:
            message.append("1")
        else:
            message.append("0")

    return "".join(message)


def extract_message_algorithm4(watermark):
    # Wyodrębnienie bitów wiadomości z sekwencji otwarcie-zamknięcie-otwarcie w znacznikach FONT
    font_tags = re.findall(r"<font.*?>", watermark)
    message = []
    for i in range(len(font_tags)):
        tag = font_tags[i]
        if i + 1 < len(font_tags) and font_tags[i + 1] == "</font><font>":
            message.append("0")
        else:
            message.append("1")

    return "".join(message)


def hide_message(cover, message, algorithm):
    if algorithm == 1:
        return hide_message_algorithm1(cover, message)
    elif algorithm == 2:
        return hide_message_algorithm2(cover, message)
    elif algorithm == 3:
        return hide_message_algorithm3(cover, message)
    elif algorithm == 4:
        return hide_message_algorithm4(cover, message)
    else:
        print("Error: Invalid algorithm number.")
        sys.exit(1)


def extract_message(watermark, algorithm):
    if algorithm == 1:
        return extract_message_algorithm1(watermark)
    elif algorithm == 2:
        return extract_message_algorithm2(watermark)
    elif algorithm == 3:
        return extract_message_algorithm3(watermark)
    elif algorithm == 4:
        return extract_message_algorithm4(watermark)
    else:
        print("Error: Invalid algorithm number.")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: stegano.py <option> <algorithm>")
        sys.exit(1)

    option = sys.argv[1]
    algorithm = abs(int(sys.argv[2]))

    if option == "-e":
        with open("mess.txt", "r") as f:
            message = f.read().strip()
        with open("cover.html", "r") as f:
            cover = f.read()

        watermark = hide_message(cover, message, algorithm)

        with open("watermark.html", "w") as f:
            f.write(watermark)

        print("Message hidden successfully.")

    elif option == "-d":
        print("Extracting message...")
        with open("watermark.html", "r") as f:
            watermark = f.read()
            print(watermark)

        message = extract_message(watermark, algorithm)

        with open("detect.txt", "w") as f:
            f.write(message)

        print("Message extracted successfully.")

    else:
        print("Error: Invalid option.")
        sys.exit(1)


if __name__ == "__main__":
    main()
