# Technika: przyjęcie na sztywno, że celem ukrywania wiadomości jest np. przesyłanie tajnego klucza o z góry ustalonej długości 64 bity.
import re
import sys

# Bartosz Brodowski 278830


def hex_to_bit(message):
    if len(message) == 64 and re.fullmatch(re.compile(r"[0-1]+"), message):
        return message
    elif len(message) == 16 and re.fullmatch(re.compile(r"[A-F0-9]+"), message):
        bit_message = ""
        for hex_digit in message:
            bit_message += bin(int(hex_digit, 16))[2:].zfill(4)
        return bit_message
    else:
        raise (
            Exception(
                "Message must be EITHER 16 characters long hex digits string OR 64 charcters long bit digits string"
            )
        )


def bit_to_hex(message):
    if len(message) != 64 or not re.fullmatch(re.compile(r"[0-1]+"), message):
        raise (Exception("Bit message must be 64 characters long binary digits string"))
    else:
        bin_numbers_list = [message[i : i + 4] for i in range(0, len(message), 4)]
        bin_numbers_list = [
            hex(int(bin_num, 2)).upper()[2:] for bin_num in bin_numbers_list
        ]
        message = "".join(bin_numbers_list)
        return message


def first_hide_message_algorithm(cover, message):
    if len(cover) < 64:
        raise (Exception("Cover must have at least 64 lines"))
    else:
        bit_message = hex_to_bit(message)
        cover_transformer = cover.split("\n")
        cover_enc = []
        cover_head = cover_transformer[:64]
        cover_tail = cover_transformer[64:]
        for bit, line in zip([*bit_message], cover_head):
            new_line = line.rstrip()
            if int(bit) == 1:
                new_line += " \n"
            else:
                new_line += "\n"
            cover_enc.append(new_line)
        watermark = "".join(cover_enc) + "".join(cover_tail)
        return watermark


def second_hide_message_algorithm(cover, message):
    space_count = cover.count(" ") - cover.count("    ") * 4
    if space_count < 64:
        print("Not enough spaces in the cover for the entire message")
        sys.exit(1)
    else:
        bit_message = hex_to_bit(message)
        watermark = cover.split("\n")
        for i, line in enumerate(watermark):
            for index, char in enumerate(line):
                if len(bit_message) == 0:
                    break
                elif (
                    watermark[i][index] == " "
                    and index + 1 < len(line)
                    and not (
                        watermark[i][index + 1] == " " or watermark[i][index - 1] == " "
                    )
                ):
                    if bit_message[0] == "1":
                        watermark[i] = (
                            watermark[i][:index] + "  " + watermark[i][index + 1 :]
                        )
                    bit_message = bit_message[1:]
        watermark = "\n".join(watermark)
        return watermark


def third_hide_message_algorithm(cover, message):
    paragraph_tags = re.findall(r"<p.*?>", cover)
    if len(paragraph_tags) < 64:
        raise (Exception("Cover must have at least 64 <p></p> tags"))
    else:
        watermark = cover.replace("margin-botom", "margin-bottom").replace(
            "lineheight", "line-height"
        )
        messageBinary = hex_to_bit(message)
        for bit_index, tag in enumerate(paragraph_tags):
            if bit_index < 64:
                if messageBinary[bit_index] == "0":
                    watermark = watermark.replace(
                        tag, '<p style="margin-bottom: 0; line-height: 0;">', 1
                    )
                else:
                    watermark = watermark.replace(
                        tag, '<p style="margin-botom: 0; lineheight: 0;">', 1
                    )
        return watermark


def fourth_hide_message_algorithm(cover, message):
    font_tags = re.findall(r"<font.*?>*</font>", cover)
    if len(font_tags) < 64:
        print("Must be 64 fonts.")
        sys.exit(1)
    messageBinary = hex_to_bit(message)
    watermark = cover

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


def first_extract_message_algorithm(watermark):
    if len(watermark) < 64:
        raise (Exception("Watermark must have at least 64 lines"))
    else:
        watermark_transformed = watermark.split("\n")
        bit_message_dec = ""
        watermark_head = watermark_transformed[:64]
        for line in watermark_head:
            if line[-1] == " ":
                bit_message_dec += "1"
            else:
                bit_message_dec += "0"
        message = bit_to_hex(bit_message_dec)
        return message


def second_extract_message_algorithm(watermark):
    watermark = watermark.split("\n")
    message_decrypted = ""
    for line in watermark:
        watermark_no_t = line.lstrip()
        for i, _ in enumerate(watermark_no_t):
            if len(message_decrypted) == 64:
                break
            if watermark_no_t[i] == " " and watermark_no_t[i + 1] == " ":
                message_decrypted += "1"
            if (
                watermark_no_t[i - 1] != " "
                and watermark_no_t[i] == " "
                and watermark_no_t[i + 1] != " "
            ):
                message_decrypted += "0"
        if len(message_decrypted) == 64:
            break
    message = bit_to_hex(message_decrypted)
    return message


def third_extract_message_algorithm(watermark):
    matches = re.findall(r'<p style="(.*?)">', watermark)
    message = []
    for match in matches:
        if "margin-botom" in match and "lineheight" in match:
            message.append("1")
        else:
            message.append("0")

    return hex(int("".join(message), 2))[2:]


def fourth_extract_message_algorithm(watermark):
    font_tags = re.findall(
        r"<font></font><font.*?>*</font>|<font.*?>*</font><font></font>", watermark
    )
    message = []
    for tag in font_tags:
        if tag[:13] == "<font></font>":
            message.append("0")
        else:
            message.append("1")
    return hex(int("".join(message), 2))[2:]


def hide_message(cover, message, algorithm):
    if algorithm == 1:
        return first_hide_message_algorithm(cover, message)
    elif algorithm == 2:
        return second_hide_message_algorithm(cover, message)
    elif algorithm == 3:
        return third_hide_message_algorithm(cover, message)
    elif algorithm == 4:
        return fourth_hide_message_algorithm(cover, message)
    else:
        print("Invalid algorithm number")
        sys.exit(1)


def extract_message(watermark, algorithm):
    if algorithm == 1:
        return first_extract_message_algorithm(watermark)
    elif algorithm == 2:
        return second_extract_message_algorithm(watermark)
    elif algorithm == 3:
        return third_extract_message_algorithm(watermark)
    elif algorithm == 4:
        return fourth_extract_message_algorithm(watermark)
    else:
        print("Invalid algorithm number")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Wrong parameters, expected 2")
        sys.exit(1)

    algorithm = abs(int(sys.argv[2]))
    option = sys.argv[1]

    if option == "-e":
        with open("mess.txt", "r") as f:
            message = f.read().strip()
        with open("cover.html", "r") as f:
            cover = f.read()
        watermark = hide_message(cover, message, algorithm)
        with open("watermark.html", "w") as f:
            f.write(watermark)
            print("Message hidden successfully")
    elif option == "-d":
        with open("watermark.html", "r") as f:
            watermark = f.read()
        message = extract_message(watermark, algorithm)
        with open("detect.txt", "w") as f:
            f.write(message.upper())
            print("Message extracted successfully")
    else:
        print("Invalid option")
        sys.exit(1)


if __name__ == "__main__":
    main()
