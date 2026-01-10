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
def normalize_pixels(pixel_arr):
    pixel_arr = pixel_arr.astype(float)  # convert from int to float

    pixel_arr -= np.min(pixel_arr)  # adjust range: start from 0
    max_val = np.max(pixel_arr)

    if max_val == 0:  # check for empty image before dividing
        return None

    pixel_arr /= max_val  # adjust range: 0 to 1
    pixel_arr *= 255  # adjust range: 0 to 255

    return pixel_arr.astype(np.uint8)


# process dicom; return PIL image
def load_dcm(dcm_path):
    dcm = pydicom.dcmread(dcm_path)
    dcm_arr = dcm.pixel_array

    if dcm.PhotometricInterpretation == "MONOCHROME1":  # fix inverted images
        dcm_arr = np.max(dcm_arr) - dcm_arr

    normalized_dcm = normalize_pixels(dcm_arr)
    if normalized_dcm is None:  # empty image
        return None

    return Image.fromarray(normalized_dcm)
