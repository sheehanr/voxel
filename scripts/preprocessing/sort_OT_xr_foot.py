import random
from pathlib import Path

from image_utils import process_image
from shared import get_filepaths, get_subdirs, init_single_dir, split_data
from tqdm import tqdm

DATASET_NAME = "OT_xr_foot"
CLASS_NAME = "xr_foot"
SUFFIX = "_OT"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR / "all_category/all_category"


def main():
    random.seed(42)

    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)
    subdirs = get_subdirs(SRC_DIR)
    filepaths = get_filepaths(SRC_DIR, subdirs)
    train_files, val_files = split_data(filepaths)

    for filepath in tqdm(train_files, desc="Processing train files"):
        process_image(filepath, train_dst, check_inversion=False)

    for filepath in tqdm(val_files, desc="Processing val files"):
        process_image(filepath, val_dst, check_inversion=False)


if __name__ == "__main__":
    main()
