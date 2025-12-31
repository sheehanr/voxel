import os

import numpy as np
import pydicom
from PIL import Image


# load image and standardize; return PIL image
def load_image(filepath, img_size=(256, 256)):
    img = Image.open(filepath).convert("L")  # convert to grayscale
    img = img.resize(img_size)

    return img


# process dicom; return PIL image
def load_dcm(dcm_path, img_size=(256, 256)):
    dcm = pydicom.dcmread(dcm_path)
    original_pixels = dcm.pixel_array.astype(float)  # convert int to float

    # fix inverted images
    if dcm.PhotometricInterpretation == "MONOCHROME1":
        original_pixels = np.max(original_pixels) - original_pixels

    # normalize
    normalized_pixels = original_pixels - np.min(original_pixels)  # adjust range: start from 0
    if np.max(normalized_pixels) == 0:  # check for empty image before dividing
        return None
    normalized_pixels = normalized_pixels / np.max(normalized_pixels)  # adjust range: 0 to 1
    normalized_pixels = (normalized_pixels * 255).astype(np.uint8)  # adjust range: 0 to 255

    # standardize
    img = Image.fromarray(normalized_pixels, mode="L")
    img = img.resize(img_size)

    return img


def process_image(filepath, dst_dir, img_size=(256, 256)):
    if not os.path.exists(filepath):
        return

    # split file into name and extension
    file = os.path.basename(filepath)
    filename = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1].lower()
    img = None

    # handle according to file extension
    if ext == ".dcm":
        img = load_dcm(filepath, img_size)

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = load_image(filepath, img_size)

    if img is None:  # incorrect extension or bad file
        return

    # save as png
    dst_name = filename + ".png"
    dst_path = os.path.join(dst_dir, dst_name)
    img.save(dst_path)
