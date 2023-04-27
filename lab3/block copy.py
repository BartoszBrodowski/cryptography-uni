# Bartosz Brodowski

from PIL import Image
import hashlib as hl

image = Image.open("plain.bmp")

# Przekształcenie na bajty
image_data = image.tobytes()

# Wymiary obrazu (szerokość i wysokość)
w, h = image.size

# new_image to tablica jednowymiarowa zawierająca zaszyfrowane wartości pikseli
new_image = []
keys = []
block_size = 8

for x in range(block_size):
    key = hl.sha1(str(x**15 + x).encode("UTF-8")).digest()
    keys.append(key)

for x in range(w):
    for y in range(h):
        index = x * h + y
        # Stara wartość piksela
        old_pixel_value = image_data[index]
        new_pixel_value = old_pixel_value ^ keys[x % block_size][y % block_size]
        new_image.append(new_pixel_value)

# Szyfrowanie ECB (fill dodaje kolorów RGB dla każdego piksela)
fill = [i for n in range(3) for i in new_image]
# "L" outputuje obraz w bieli i czerni, (w,h) określa rozmiar obrazu
ecb_image = Image.new("RGB", (w, h))
# Wypełnienie zdjęcia bitami z tablicy fill (każdy pixel ma 3 bajty)
ecb_image.frombytes(bytes(fill))
# Zapisanie obrazu do pliku
ecb_image.save("ecb_crypto.bmp")

with open("key.txt") as key:
    new_key = key.read()
    new_key = int(new_key) % 256

new_image = [image_data[0] ^ new_key]
for x in range(w * h):
    new_image.append(new_image[x - 1] ^ image_data[x] ^ keys[x % 64 // 8][x % 8])


# Szyfrowanie CBC
fill = [i for n in range(3) for i in new_image]
cbc_image = Image.new("L", (w, h))
cbc_image.frombytes(bytes(fill))
cbc_image.save("cbc_crypto.bmp")
