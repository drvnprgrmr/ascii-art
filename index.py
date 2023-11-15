from PIL import Image
from time import sleep

img = Image.open("./images/ascii-pineapple.jpg")

img = img.resize((200, 200))

width, height = img.size

print("Image loaded successfully!")
print(f"Image size: {width} x {height}")

sleep(.5)

# Get pixels of image
pixels = list(img.getdata())
pixel_grid = [ pixels[i * width: (i + 1) * width] for i in range(height)]

brightness_matrix = [[sum(pixel) / 3 for pixel in row] for row in pixel_grid]

ASCII_BRIGHTNESS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Convert brightness matrix to ascii matrix
ascii_matrix = []
for row in brightness_matrix:
    ascii_row = []
    for brightness in row:
        ascii_idx = int(brightness / 255 * len(ASCII_BRIGHTNESS))
        ascii_char = ASCII_BRIGHTNESS[ascii_idx]
        ascii_row.append(ascii_char * 3)
    ascii_matrix.append(ascii_row)

for row in ascii_matrix:
    print("".join(row))
    sleep(.05)
