import numpy as np
import pydicom
from PIL import Image


# convert to grayscale and resize
def standardize_image(png_path, target_size=(256, 256)):
    img = Image.open(png_path).convert("L")
    img = img.resize(target_size)

    return img


# normalize DICOM and convert to PNG
def dcm_to_png(dcm_path, target_size=(256, 256)):
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
    png = png.resize(target_size)

    return png
