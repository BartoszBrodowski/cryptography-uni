Hello! I will explain this Python code to you step by step, as if I were talking to a child, so that you can understand it easily. Let's break down the code into smaller parts and go through each of them.

### 1. Import the necessary libraries:

```python
from PIL import Image
import hashlib
```

This code imports the "Image" module from the "PIL" library and the "hashlib" library. We will use the "Image" module to work with images and the "hashlib" library to create hash functions.

### 2. Load the input image:

```python
input_image = Image.open("plain.bmp")
```

This line opens the image file called "plain.bmp" and stores it in the variable "input_image".

### 3. Get the image data and size:

```python
image_data = input_image.tobytes()
width, height = input_image.size
```

Here, we convert the image to a series of bytes and store it in "image_data". We also get the width and height of the image and store them in "width" and "height".

### 4. Prepare the new data and keys:

```python
new_data = []
keys = []
block = 8

for x in range(block):
    key = hashlib.sha1(str(x ** 15 + x).encode("UTF-8")).digest()
    keys.append(key)
```

We create two empty lists called "new_data" and "keys". The "block" variable is set to 8, which means each block of the image will have 8 pixels. Then, we create 8 hash keys using the SHA-1 hash function and store them in the "keys" list.

### 5. Modify the image data using the keys:

```python
for x in range(width):
    for y in range(height):
        index = x * height + y
        old_value = image_data[index]
        new_value = old_value ^ keys[x % block][y % block]
        new_data.append(new_value)
```

In these nested loops, we go through each pixel of the image. We calculate the index of the pixel in the image data, get its original value, and calculate a new value by XORing it with the corresponding key. We then add the new value to the "new_data" list.

### 6. Save the encrypted image in ECB mode:

```python
fill = [i for n in range(3) for i in new_data]
output_ecb = Image.new("RGB", (width, height))
output_ecb.frombytes(bytes(fill))
output_ecb.save("ecb_crypto.bmp")
```

We create a new list called "fill" by repeating each value in "new_data" three times. We then create a new image called "output_ecb" with the same size as the input image, fill it with the new data, and save it as "ecb_crypto.bmp".

### 7. Encrypt the image in CBC mode:

```python
new_key = 274991 % 256
new_data = [image_data[0] ^ new_key]
for x in range(width * height):
    new_data.append(new_data[x - 1] ^ image_data[x] ^ keys[x % 64 // 8][x % 8])

fill = [i for n in range(3) for i in new_data]

output_cbc = Image.new("RGB", (width, height))
output_cbc.frombytes(bytes(fill))
output_cbc.save("cbc_crypto.bmp")
```

First, we create a new key called "new_key" and initialize "new_data" with the first encrypted pixel. Then, we loop through each pixel of the image and modify its value using the new key, the previous pixel's value, and the corresponding hash key. We add the new values to the "new_data" list.

Next, we create a new list called "fill" by repeating each value in "new_data" three times. We then create a new image called "output_cbc" with the same size as the input image, fill it with the new data, and save it as "cbc_crypto.bmp".

That's it! This code reads an image, encrypts it in two different block cipher modes (ECB and CBC), and saves the encrypted images as new files. By comparing the encrypted images, you can see how the ECB mode is less secure than the CBC mode, as the simple patterns in the original image are still visible in the ECB-encrypted image.
