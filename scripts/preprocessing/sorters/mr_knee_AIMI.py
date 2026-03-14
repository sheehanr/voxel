from pathlib import Path

import numpy as np
from PIL import Image

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
VAL_SRC = SRC_DIR / "val"


def main():
    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)

    train_subdirs = get_subdirs(TRAIN_SRC)
    val_subdirs = get_subdirs(VAL_SRC)

    train_filepaths = get_filepaths(TRAIN_SRC, train_subdirs)
    val_filepaths = get_filepaths(VAL_SRC, val_subdirs)


if __name__ == "__main__":
    main()
