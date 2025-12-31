import os
import random

from image_utils import process_image
from shared import get_subdirectories, list_filepaths, setup_directories, split_dataset
from tqdm import tqdm

DATASET_NAME = "MG_xr_knee"
PYTORCH_CLASS = "xr_knee"
CLASS_SUBDIR = "xr_knee_MG"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
UNSORTED_DIR = os.path.join(DATASET_DIR, "OS Collected Data")

SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, PYTORCH_CLASS)
SORTED_VAL_DIR = os.path.join(VAL_DIR, PYTORCH_CLASS)


def main():
    random.seed(42)

    target_train_dir, target_val_dir = setup_directories(PYTORCH_CLASS, CLASS_SUBDIR, SORTED_TRAIN_DIR, SORTED_VAL_DIR)
    subdirs_list = get_subdirectories(UNSORTED_DIR)
    all_filepaths = list_filepaths(UNSORTED_DIR, subdirs_list)
    selected_train_filepaths, selected_val_filepaths = split_dataset(all_filepaths)

    for filepath in tqdm(selected_train_filepaths):
        process_image(filepath, target_train_dir)

    for filepath in tqdm(selected_val_filepaths):
        process_image(filepath, target_val_dir)


if __name__ == "__main__":
    main()
