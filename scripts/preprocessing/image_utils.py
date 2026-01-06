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
def standardize_pil(img, img_size=IMG_SIZE, check_inversion=True):
    img = img.convert("L")  # convert to grayscale

    if check_inversion:
        img.thumbnail(img_size, Image.Resampling.LANCZOS)  # shrink without distorting
        img = inversion_helper(img)  # check for inversion

    img = ImageOps.pad(img, img_size, method=Image.Resampling.LANCZOS, color=0)  # pad to preserve aspect ratio

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

    if dcm.PhotometricInterpretation == "MONOCHROME1":  # fix inverted images
        pixels = np.max(pixels) - pixels

    normalized_pixels = normalize_pixels(pixels)
    if normalized_pixels is None:  # empty image
        return None

    return Image.fromarray(normalized_pixels)


# handle file according to extension; return img and check_inversion
def handle_file(filepath, ext, check_inversion):
    if ext == ".dcm":
        return load_dcm(filepath), False

    elif ext in [".jpg", ".jpeg", ".png"]:
        return Image.open(filepath), check_inversion

    return None, True


# get destination path
def get_dst_path(filename, dst_dir, prefix, custom_name):
    if custom_name:
        filename = custom_name

    if prefix:
        filename = f"{prefix}{filename}"

    dst_name = f"{filename}.png"

    return os.path.join(dst_dir, dst_name)


# load, process, and save image
def process_image(filepath, dst_dir, prefix=None, custom_name=None, check_inversion=True, img_size=IMG_SIZE):
    if not os.path.exists(filepath):
        print(f"ERROR [process_image]: {filepath} not found")
        return

    os.makedirs(dst_dir, exist_ok=True)
    filename, ext = os.path.splitext(os.path.basename(filepath))

    img, check_inversion = handle_file(filepath, ext, check_inversion)
    if img is None:
        return

    # standardize and save as png
    img = standardize_pil(img, img_size, check_inversion)
    dst_path = get_dst_path(filename, dst_dir, prefix, custom_name)
    img.save(dst_path)
