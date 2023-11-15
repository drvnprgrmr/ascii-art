from PIL import Image

img = Image.open("./images/ascii-pineapple.jpg")

width, height = img.size

pixels = list(img.getdata())
pixel_grid = [ pixels[i * width: (i + 1) * width] for i in range(height)]

print(len(pixels))
if __name__ == "__main__":
    print("Image loaded successfully!")
    print(f"Image size: {width} x {height}")
    for row in pixel_grid:
        print(row)