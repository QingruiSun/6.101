"""
6.1010 Spring '23 Lab 2: Image Processing 2
"""

#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image


def get_pixel(image, row, col, boundary_behavior="extend"):
    height = image["height"]
    width = image["width"]
    if row >= 0 and row < height and col >= 0 and col < width:
        return image["pixels"][row * width + col]
    if boundary_behavior == "zero":
        return 0
    if boundary_behavior == "extend":
        if row <= 0:
            if col <= 0:
                return image["pixels"][0]
            if col >= width:
                return image["pixels"][width - 1]
            return image["pixels"][col]
        if row >= height - 1:
            if col <= 0:
                return image["pixels"][width * (height - 1)]
            if col >= width:
                return image["pixels"][width * height - 1]
            return image["pixels"][(height - 1) * width + col]
        if col < 0:
            return image["pixels"][row * width]
        return image["pixels"][row * width + width - 1]
    if boundary_behavior == "wrap":
        row = row % height
        col = col % width
        return images["pixles"][row * width + col]


def set_pixel(image, row, col, color):
    image["pixels"][row * image["width"] + col] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [],
    }
    result["pixels"] = [0] * (image["height"] * image["width"])
    for row in range(image["height"]):
        for col in range(image["width"]):
            color = get_pixel(image, row, col)
            new_color = func(color)
            set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 255 - color)


# HELPER FUNCTIONS


def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    """
    if (
        boundary_behavior != "zero"
        and boundary_behavior != "wrap"
        and boundary_behavior != "extend"
    ):
        return None
    width = image["width"]
    height = image["height"]
    result_img = {"width": width, "height": height, "pixels": [0] * (width * height)}
    side_length = int(math.sqrt(len(kernel)))
    for i in range(height):
        for j in range(width):
            half_length = side_length // 2
            result_pixel = 0
            for row in range(-half_length, half_length + 1):
                for col in range(-half_length, half_length + 1):
                    originated_pixel = get_pixel(
                        image, i + row, j + col, boundary_behavior
                    )
                    if i == 5 and j == 5:
                        print(originated_pixel)
                    result_pixel += (
                        originated_pixel
                        * kernel[(row + half_length) * side_length + col + half_length]
                    )
                    if i == 5 and j == 5:
                        print(result_pixel)
            result_img["pixels"][i * width + j] = result_pixel
    print(result_img)
    return result_img


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for i, pixel in enumerate(image["pixels"]):
        image["pixels"][i] = int(round(image["pixels"][i]))
        if image["pixels"][i] > 255:
            image["pixels"][i] = 255
        if image["pixels"][i] < 0:
            image["pixels"][i] = 0
    return image


# FILTERS


def get_blur_kernel(kernel_size):
    kernel = []
    for i in range(kernel_size * kernel_size):
        kernel.append(1 / (kernel_size * kernel_size))
    return kernel


def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)

    # then compute the correlation of the input image with that kernel

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    kernel = get_blur_kernel(kernel_size)
    blurred_img = correlate(image, kernel, "extend")
    return round_and_clip_image(blurred_img)


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES


def sharpened(image, kernel_size):
    kernel = get_blur_kernel(kernel_size)
    blurred_img = correlate(image, kernel, "extend")
    height = image["height"]
    width = image["width"]
    sharpened_img = {"height": height, "width": width, "pixels": [0] * (height * width)}
    for i in range(height):
        for j in range(width):
            index = i * width + j
            sharpened_img["pixels"][index] = (
                2 * image["pixels"][index] - blurred_img["pixels"][index]
            )
    return round_and_clip_image(sharpened_img)


def edges(image):
    row_kernel = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    col_kernel = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    height = image["height"]
    width = image["width"]
    row_correlate_img = correlate(image, row_kernel, "extend")
    col_correlate_img = correlate(image, col_kernel, "extend")
    result_img = {"height": height, "width": width, "pixels": [0] * (height * width)}
    for i in range(height):
        for j in range(width):
            index = i * width + j
            result_img["pixels"][index] = math.sqrt(
                row_correlate_img["pixels"][index] ** 2
                + col_correlate_img["pixels"][index] ** 2
            )
    return round_and_clip_image(result_img)


# VARIOUS FILTERS


def get_channel(image, channel):
    height = image["height"]
    width = image["width"]
    grey_image = {"height": height, "width": width, "pixels": [0] * (height * width)}
    for i in range(height):
        for j in range(width):
            index = i * width + j
            grey_image["pixels"][index] = image["pixels"][index][channel]
    return grey_image


def assemble_color_image(r_image, g_image, b_image):
    height = r_image["height"]
    width = r_image["width"]
    color_image = {"height": height, "width": width, "pixels": []}
    for i in range(height):
        for j in range(width):
            index = i * width + j
            color_image["pixels"].append(
                (
                    r_image["pixels"][index],
                    g_image["pixels"][index],
                    b_image["pixels"][index],
                )
            )
    return color_image


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """

    def color_filter(image):
        r_image = get_channel(image, 0)
        g_image = get_channel(image, 1)
        b_image = get_channel(image, 2)
        r_filter_image = filt(r_image)
        g_filter_image = filt(g_image)
        b_filter_image = filt(b_image)
        return assemble_color_image(r_filter_image, g_filter_image, b_filter_image)

    return color_filter


def make_blur_filter(kernel_size):
    def func(image):
        return blurred(image, kernel_size)

    return func


def make_sharpen_filter(kernel_size):
    def func(image):
        return sharpened(image, kernel_size)

    return func


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """

    def filter(image):
        for f in filters:
            image = f(image)
        return image

    return filter


# SEAM CARVING

# Main Seam Carving Implementation

# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    height = image["height"]
    width = image["width"]
    grey_image = {"height": height, "width": width, "pixels": [0] * (height * width)}
    for i in range(height):
        for j in range(width):
            index = i * width + j
            grey_image["pixels"][index] = round(
                image["pixels"][index][0] * 0.299
                + image["pixels"][index][1] * 0.587
                + image["pixels"][index][2] * 0.114
            )
    return grey_image


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    height = energy["height"]
    width = energy["width"]
    cumulative_energy = {
        "height": height,
        "width": width,
        "pixels": [0] * (height * width),
    }
    for i in range(width):
        cumulative_energy["pixels"][i] = energy["pixels"][i]
    for i in range(1, height):
        for j in range(width):
            index = i * width + j
            left = 100000
            mid = 0
            right = 100000
            if j > 0:
                left = cumulative_energy["pixels"][index - width - 1]
            if j < width - 1:
                right = cumulative_energy["pixels"][index - width + 1]
            mid = cumulative_energy["pixels"][index - width]
            cumulative_energy["pixels"][index] = min(left, mid, right) + energy["pixels"][index]
    return cumulative_energy


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    height = cem["height"]
    width = cem["width"]
    indices = []
    min_energy = 10000
    min_index = -1
    for i in range(0, width):
        index = width * (height - 1) + i
        if cem["pixels"][index] < min_energy:
            min_energy = cem["pixels"][index]
            min_index = index
    indices.append(min_index)
    prev_index = min_index
    for i in range(height - 2, -1, -1):
        mid_value = cem["pixels"][prev_index - width]
        left_value = 10000
        right_value = 10000
        if prev_index % width != 0:
            left_value = cem["pixels"][prev_index - width - 1]
        if prev_index % width != (width - 1):
            right_value = cem["pixels"][prev_index - width + 1]
        min_value = min(left_value, mid_value, right_value)
        if left_value == min_value:
            min_index = prev_index - width - 1
        elif mid_value == min_value:
            min_index = prev_index - width
        else:
            min_index = prev_index - width + 1
        indices.append(min_index)
        prev_index = min_index
    reverse_indices = []
    for i in range(height - 1, -1, -1):
        reverse_indices.append(indices[i])
    return reverse_indices


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    height = image["height"]
    width = image["width"]
    new_image = {"height": height, "width": width - 1, "pixels": []}
    for i in range(height):
        for j in range(width):
            index = i * width + j
            if index != seam[i]:
                new_image["pixels"].append(image["pixels"][index])
    return new_image

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    f = []
    f.append(greyscale_image_from_color_image)
    f.append(compute_energy)
    f.append(cumulative_energy_map)
    f.append(minimum_energy_seam)
    filters = filter_cascade(f)
    for i in range(ncols):
        indices = filters(image)
        new_image = image_without_seam(image, indices)
        image = new_image
    return image

# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass
