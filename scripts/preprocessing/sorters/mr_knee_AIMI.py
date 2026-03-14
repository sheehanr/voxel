from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

from scripts.preprocessing.utils import (
    get_dst_path,
    get_filepaths,
    get_subdirs,
    init_single_dir,
    normalize_pixels,
    standardize_pil,
)

DATASET_NAME = "mr_knee_AIMI"
CLASS_NAME = "mr_knee"
SUFFIX = "_AIMI"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR / "MRNet-v1.0"

TRAIN_SRC = SRC_DIR / "train"
VAL_SRC = SRC_DIR / "valid"


def handle_npy(filepaths, dst_dir, tqdm_desc="Processing files"):
    for f in tqdm(filepaths, desc=tqdm_desc):
        if f.suffix.lower() != ".npy" or not f.exists():
            continue

        plane = f.parent.name  # "axial"/"coronal"/"sagittal"
        file_id = f.stem  # "0001"

        vol = np.load(f)
        for i in range(vol.shape[0]):
            slice_arr = vol[i]
            normalized_slice = normalize_pixels(slice_arr)
            if normalized_slice is None:
                continue

            slice_img = Image.fromarray(normalized_slice)
            img = standardize_pil(slice_img, check_inversion=False)

            filename = f"{file_id}_{plane}_{i}"
            dst_path = get_dst_path(filename, dst_dir, None, None)
            img.save(dst_path)


def main():
    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)

    train_subdirs = get_subdirs(TRAIN_SRC)
    val_subdirs = get_subdirs(VAL_SRC)

    train_filepaths = get_filepaths(TRAIN_SRC, train_subdirs)
    val_filepaths = get_filepaths(VAL_SRC, val_subdirs)

    handle_npy(train_filepaths, train_dst, "Processing train files")
    handle_npy(val_filepaths, val_dst, "Processing val files")


if __name__ == "__main__":
    main()
