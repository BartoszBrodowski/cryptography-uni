# Bartosz Brodowski, 278830

import re
import sys

def hide_message_algorithm1(cover, message):
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
    space_count = cover.count(" ") - cover.count("    ") * 4
    if space_count < 64:
        print("Error: Not enough spaces in the cover for the entire message.")
        sys.exit(1)

    messageBinary = bin(int(message, 16))[2:]
    print(messageBinary)
    watermark = cover.split("\n")
    for i, line in enumerate(watermark):
        for index, char in enumerate(line):
            if len(messageBinary) == 0:
                break
            elif (
                watermark[i][index] == " "
                and index + 1 < len(line)
                and not (
                    watermark[i][index + 1] == " " or watermark[i][index - 1] == " "
                )
            ):
                if messageBinary[0] == "1":
                    watermark[i] = (
                        watermark[i][:index] + "  " + watermark[i][index + 1 :]
                    )
                messageBinary = messageBinary[1:]
    watermark = "\n".join(watermark)
    return watermark


def hide_message_algorithm3(cover, message):
    paragraph_tags = re.findall(r"<p.*?>", cover)
    if len(paragraph_tags) < 64:
        print("Error: Not enough paragraph tags in the cover for the entire message.")
        sys.exit(1)
    print(paragraph_tags)
    watermark = cover
    messageBinary = bin(int(message, 16))[2:]

    for i, tag in enumerate(paragraph_tags):
        if i < 64:
            if messageBinary[i] == "0":
                watermark = watermark.replace(
                    tag,
                    '<p style="margin-bottom: 0; line-height: 0;">',
                    1,
                )
            else:
                watermark = watermark.replace(
                    tag,
                    '<p style="margin-botom: 0; lineheight: 0;">',
                    1,
                )
    print(watermark)
    return watermark


def hide_message_algorithm4(cover, message):
    font_tags = re.findall(r"<font.*?>*</font>", cover)
    print(font_tags)
    if len(font_tags) < 64:
        print("Error: Musi byc 64 fontow.")
        sys.exit(1)

    messageBinary = bin(int(message, 16))[2:]
    watermark = cover
    print(font_tags)

    def replace_nth_occurrence(text, search, replacement, occurrence):
        count = 0
        index = -1

        while count < occurrence:
            index = text.find(search, index + 1)
            if index == -1:
                break
            count += 1

        if count == occurrence:
            return text[:index] + text[index:].replace(search, replacement, 1)

        return text

    siema = cover

    for i, tag in enumerate(font_tags):
        if i < 64:
            if messageBinary[i] == "0":
                watermark = replace_nth_occurrence(
                    watermark, tag, "<font></font>" + tag, i + 1
                )
            else:
                watermark = replace_nth_occurrence(
                    watermark, tag, tag + "<font></font>", i + 1
                )
    return watermark


def extract_message_algorithm1(watermark):
    lines = watermark.split("\n")
    lines = lines[:16]
    message = ""
    for line in lines:
        spaces_count = len(line) - len(line.rstrip())
        message += hex(spaces_count)[-1]
    return message


def extract_message_algorithm2(watermark):
    watermark = watermark.replace("    ", "")
    message = []
    bits = 64
    for i, char in enumerate(watermark):
        if char == " " and len(message) < bits and i > 0:
            match watermark[i - 1]:
                case " ":
                    message.append("1")
                case _:
                    if watermark[i + 1] != " ":
                        message.append("0")
    szestanskowy = hex(int("".join(message), 2))[2:]
    return szestanskowy


def extract_message_algorithm3(watermark):
    # Wyodrębnienie bitów wiad
    matches = re.findall(r'<p style="(.*?)">', watermark)
    message = []
    for match in matches:
        if "margin-botom" in match or "lineheight" in match:
            message.append("1")
        else:
            message.append("0")

    return hex(int("".join(message), 2))[2:]


def extract_message_algorithm4(watermark):
    font_tags = re.findall(
        r"<font></font><font.*?>*</font>|<font.*?>*</font><font></font>", watermark
    )
    print(font_tags)
    message = []
    for tag in font_tags:
        if tag[:13] == "<font></font>":
            message.append("0")
        else:
            message.append("1")
    return hex(int("".join(message), 2))[2:]


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

        message = extract_message(watermark, algorithm)

        with open("detect.txt", "w") as f:
            f.write(message)

        print("Message extracted successfully.")

    else:
        print("Error: Invalid option.")
        sys.exit(1)


if __name__ == "__main__":
    main()
