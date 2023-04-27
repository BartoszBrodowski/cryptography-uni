# Bartosz Brodowski 2023
import hashlib as hl
from PIL import Image

image = Image.open("plain.bmp")
image_data = image.tobytes()

# Przekształcenie na bajty (każdy pixel zostawia 3 bajty symbolizujące wartość RGB)
new_image_data = []
keys = []
block_size = 8
w, h = image.size

# Tworzenie 8 hashowanych kluczy dla każdego pixela w bloku
for x in range(block_size):
    key = hl.sha1(str(x**15 + x).encode("UTF-8")).digest()
    keys.append(key)

for x in range(w):
    for y in range(h):
        index = x * h + y
        # Stara wartość piksela
        old_pixel_value = image_data[index]
        new_pixel_value = (
            old_pixel_value ^ keys[x % block_size**2 // block_size][y % block_size]
        )
        new_image_data.append(new_pixel_value)

# Szyfrowanie ECB
color = [i for n in range(3) for i in new_image_data]
output_ecb = Image.new("RGB", (w, h))
output_ecb.frombytes(bytes(color))
output_ecb.save("ecb_crypto.bmp")

with open("key.txt") as key:
    new_key = key.read()
    new_key = int(new_key) % 256 if new_key != "" else 278830 % 256

new_image_data = [image_data[0] ^ int(new_key)]
for x in range(w * h):
    new_image_data.append(
        new_image_data[x - 1]
        ^ image_data[x]
        ^ keys[x % block_size**2 // block_size][x % block_size]
    )

color = [i for n in range(3) for i in new_image_data]

# Szyfrowanie CBC
# "L" outputuje obraz w bieli i czerni, (w,h) określa rozmiar obrazu
output_cbc = Image.new("L", (w, h))
output_cbc.frombytes(bytes(color))
output_cbc.save("cbc_crypto.bmp")
