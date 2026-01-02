import os
import random

from image_utils import process_image
from shared import get_filepaths, get_subdirs, init_single_dir, split_data
from tqdm import tqdm

DATASET_NAME = "OT_xr_heel"
CLASS_NAME = "xr_heel"
SUFFIX = "_OT"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = os.path.join(DATASET_DIR, "all_category/all_category")


def main():
    random.seed(42)

    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)
    subdirs = get_subdirs(SRC_DIR)
    file_list = get_filepaths(SRC_DIR, subdirs)
    train_files, val_files = split_data(file_list)

    for filepath in tqdm(train_files, desc="Processing train files"):
        process_image(filepath, train_dst)

    for filepath in tqdm(val_files, desc="Processing val files"):
        process_image(filepath, val_dst)


if __name__ == "__main__":
    main()
