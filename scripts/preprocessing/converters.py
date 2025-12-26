import numpy as np
import pydicom
from PIL import Image


# normalizes DICOM then converts to PNG
def dcm_to_png(dcm_path):
    dcm = pydicom.dcmread(dcm_path)

    original_pixels = dcm.pixel_array.astype(float)  # convert int to float
    normalized_pixels = original_pixels - np.min(original_pixels)  # range starts at 0
    normalized_pixels = normalized_pixels / np.max(normalized_pixels)  # range is 0 to 1
    normalized_pixels = (normalized_pixels * 255).astype(np.uint8)  # range is 0 to 255

    png = Image.fromarray(normalized_pixels)
    return png
