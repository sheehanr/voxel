import os

import numpy as np
import pydicom
from PIL import Image, ImageOps

IMG_SIZE = (256, 256)


# check if image is inverted and fix if needed
def inversion_helper(img):
    arr = np.array(img)
    corners = np.concatenate(
        [
            arr[:20, :20].flatten(),
            arr[:20, -20:].flatten(),
            arr[-20:, :20].flatten(),
            arr[-20:, -20:].flatten(),
        ]
    )

    # invert if corners are white
    if np.median(corners) > 127:
        img = Image.fromarray(255 - arr)

    return img


# convert image to standardized format
def standardize_pil(img, img_size=IMG_SIZE):
    img = img.convert("L")  # convert to grayscale
    img = inversion_helper(img)  # check for inversion
    img = ImageOps.pad(img, img_size, color=0)  # resize and preserve aspect ratio (pad black squares)

    return img


# normalizes dicom pixel range to match regular image files
def normalize_pixels(pixel_array):
    pixels = pixel_array.astype(float)  # convert from int to float

    pixels -= np.min(pixels)  # adjust range: start from 0
    max_val = np.max(pixels)

    if max_val == 0:  # check for empty image before dividing
        return None

    pixels /= max_val  # adjust range: 0 to 1
    pixels *= 255  # adjust range: 0 to 255

    return pixels.astype(np.uint8)


# process dicom; return PIL image
def load_dcm(dcm_path):
    dcm = pydicom.dcmread(dcm_path)
    pixels = dcm.pixel_array

    # fix inverted images
    if dcm.PhotometricInterpretation == "MONOCHROME1":
        pixels = np.max(pixels) - pixels

    normalized_pixels = normalize_pixels(pixels)

    # return PIL image
    if normalized_pixels is None:
        return None

    return Image.fromarray(normalized_pixels)


# load, process, and save image
def process_image(filepath, dst_dir, prefix=None, img_size=IMG_SIZE):
    if not os.path.exists(filepath):
        return

    img = None
    filename, ext = os.path.splitext(os.path.basename(filepath))

    # handle according to file extension
    if ext == ".dcm":
        img = load_dcm(filepath)

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = Image.open(filepath)  # converts to PIL image

    if img is None:  # incorrect extension or bad file
        return

    # get destination path
    if prefix:
        filename = f"{prefix}{filename}"
    dst_name = f"{filename}.png"
    dst_path = os.path.join(dst_dir, dst_name)

    # standardize and save as png
    img = standardize_pil(img, img_size)
    img.save(dst_path)
