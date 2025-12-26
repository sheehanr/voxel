import numpy as np
import pydicom
from PIL import Image


# normalizes DICOM then converts to PNG in target size
def dcm_to_png(dcm_path, target_size=(256, 256)):
    dcm = pydicom.dcmread(dcm_path)
    original_pixels = dcm.pixel_array.astype(float)  # convert int to float

    # fixes inverted images
    if dcm.PhotometricInterpretation == "MONOCHROME1":
        original_pixels = np.max(original_pixels) - original_pixels

    normalized_pixels = original_pixels - np.min(original_pixels)  # range starts at 0

    # check for empty image before dividing
    if np.max(normalized_pixels) == 0:
        return None

    normalized_pixels = normalized_pixels / np.max(normalized_pixels)  # range is 0 to 1
    normalized_pixels = (normalized_pixels * 255).astype(np.uint8)  # range is 0 to 255

    png = Image.fromarray(normalized_pixels)
    png = png.resize(target_size)

    return png
