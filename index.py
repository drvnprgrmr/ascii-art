from PIL import Image

img = Image.open("./images/ascii-pineapple.jpg")

img_width, img_height = img.size

print("Image loaded successfully!")
print(f"Image size: {img_width} x {img_height}")