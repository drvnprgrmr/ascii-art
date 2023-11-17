from typing import List
from PIL import Image
from time import sleep
from termcolor import cprint

ASCII_CHARS = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
MAX_PIXEL_VALUE = 255
ALGORITHMS = ("average", "max_min", "luminosity", "perceived")

Matrix = List[List[int | float | str]]


def get_pixel_matrix(img: Image.Image) -> Matrix:
    """
    Gets the pixel values of an image in a matrix format.
    """
    # Convert image to a thumbnail that preserves the aspect ratio
    img.thumbnail((img.width, 200))

    # Get pixels of image
    pixels = list(img.getdata())

    return [pixels[i * img.width : (i + 1) * img.width] for i in range(img.height)]


def get_intensity_matrix(pixel_matrix: Matrix, algorithm="average") -> Matrix:
    """
    Computes an intensity matrix based on a provided algorithm.
    Note: The pixels are expected in RGB not sRGB
    """

    if algorithm not in ALGORITHMS:
        raise Exception(f"Unknown algorithm: '{algorithm}'")

    intensity_matrix = []

    for row in pixel_matrix:
        intensity_row = []

        for p in row:
            if algorithm == "average":
                intensity = sum(p) / 3.0
            elif algorithm == "max_min":
                intensity = (max(p) + min(p)) / 2.0
            else:
                # Scale rgb from 0 - 255 down to 0 - 1
                r = p[0] / MAX_PIXEL_VALUE
                g = p[1] / MAX_PIXEL_VALUE
                b = p[2] / MAX_PIXEL_VALUE

                # Calculate the luminance
                luminance = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)

                if algorithm == "luminosity":
                    intensity = luminance
                elif algorithm == "perceived":
                    if luminance <= (216 / 24389):
                        intensity = luminance * ((24389 / 27))
                    else:
                        intensity = pow(luminance, (1 / 3)) * 116 - 16

            # Add the calculated intensity to the row
            intensity_row.append(intensity)

        intensity_matrix.append(intensity_row)

    return intensity_matrix


def normalize_intensity_matrix(intensity_matrix: Matrix) -> Matrix:
    """
    Normalize the values in the matrix to be between 0 and 255.
    """
    normalized_intensity_matrix = []

    # Get the highest and lowest values in the matrix
    max_intensity = max(map(max, intensity_matrix))
    min_intensity = min(map(min, intensity_matrix))

    for row in intensity_matrix:
        normalized_row = []
        for intensity in row:
            normalized_intensity = (
                MAX_PIXEL_VALUE
                * (intensity - min_intensity)
                / float(max_intensity - min_intensity)
            )
            normalized_row.append(normalized_intensity)

        normalized_intensity_matrix.append(normalized_row)

    return normalized_intensity_matrix


def invert_intensity_matrix(intensity_matrix: Matrix) -> Matrix:
    """
    Invert a given intensity matrix making darker pixels appear lighter and
    lighter ones appear darker.
    """
    inverted_intensity_matrix = []

    for row in intensity_matrix:
        inverted_row = []
        for intensity in row:
            inverted_intensity = MAX_PIXEL_VALUE - intensity
            inverted_row.append(inverted_intensity)

        inverted_intensity_matrix.append(inverted_row)

    return inverted_intensity_matrix


def intensity_to_ascii(intensity_matrix: Matrix, ascii_chars: str) -> Matrix:
    """
    Maps given intensities to equivalent ascii characters.
    """
    ascii_matrix = []

    for row in intensity_matrix:
        ascii_row = []
        for intensity in row:
            # Get the position of the ascii character to substitute for brightness
            ascii_idx = round(intensity / MAX_PIXEL_VALUE * len(ascii_chars) - 1)
            ascii_row.append(ascii_chars[ascii_idx])

        ascii_matrix.append(ascii_row)

    return ascii_matrix


def print_ascii_matrix(ascii_matrix: Matrix, fg="white", bg="black", *, stretch=3) -> None:
    """
    Print the ascii matrix.
    """
    for row in ascii_matrix:
        # Convert row to single string
        text = "".join([char * stretch for char in row])

        # Print the ascii text
        cprint(text, fg, f"on_{bg}")

        # Add little delay after every row
        # sleep(.05)

img = Image.open("./images/ascii-pineapple.jpg")

pixel_matrix = get_pixel_matrix(img)
intensity_matrix = get_intensity_matrix(pixel_matrix, "perceived")
intensity_matrix = normalize_intensity_matrix(intensity_matrix)

# intensity_matrix = invert_intensity_matrix(intensity_matrix)
ascii_matrix = intensity_to_ascii(intensity_matrix, ASCII_CHARS)

print_ascii_matrix(ascii_matrix, "green", stretch=2)