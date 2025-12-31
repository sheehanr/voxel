import os

import numpy as np
import pydicom
from PIL import Image


# convert to grayscale and resize
def standardize_image(filepath, target_dimensions=(256, 256)):
    img = Image.open(filepath).convert("L")
    img = img.resize(target_dimensions)

    return img


# normalize DICOM and convert to PNG
def dcm_to_png(dcm_path, target_dimensions=(256, 256)):
    dcm = pydicom.dcmread(dcm_path)
    original_pixels = dcm.pixel_array.astype(float)  # convert int to float

    # fix inverted images
    if dcm.PhotometricInterpretation == "MONOCHROME1":
        original_pixels = np.max(original_pixels) - original_pixels

    # adjust range so it starts from 0
    normalized_pixels = original_pixels - np.min(original_pixels)

    # check for empty image before dividing
    if np.max(normalized_pixels) == 0:
        return None

    normalized_pixels = normalized_pixels / np.max(normalized_pixels)  # adjust range: 0 to 1
    normalized_pixels = (normalized_pixels * 255).astype(np.uint8)  # adjust range: 0 to 255

    # convert to grayscale and resize
    png = Image.fromarray(normalized_pixels, mode="L")
    png = png.resize(target_dimensions)

    return png


def process_image(filepath, save_dir, target_dimensions=(256, 256)):
    if not os.path.exists(filepath):
        return

    file = os.path.basename(filepath)
    filename = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1].lower()
    img = None

    if extension == ".dcm":
        img = dcm_to_png(filepath, target_dimensions)

    elif extension in [".jpg", ".jpeg", ".png"]:
        img = standardize_image(filepath, target_dimensions)

    if img is None:  # incorrect extension or bad file
        return

    save_filename = filename + ".png"
    save_path = os.path.join(save_dir, save_filename)
    img.save(save_path)
