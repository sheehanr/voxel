import os

import numpy as np
import pydicom
from PIL import Image


# convert PIL image to grayscale and resize
def standardize_pil(img, img_size=(256, 256)):
    return img.convert("L").resize(img_size)


# process dicom; return PIL image
def load_dcm(dcm_path):
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

    # return PIL image
    img = Image.fromarray(normalized_pixels)
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
        img = load_dcm(filepath)

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = Image.open(filepath)  # converts to PIL image

    if img is None:  # incorrect extension or bad file
        return

    # standardize and save as png
    dst_name = filename + ".png"
    dst_path = os.path.join(dst_dir, dst_name)
    img = standardize_pil(img, img_size)
    img.save(dst_path)
