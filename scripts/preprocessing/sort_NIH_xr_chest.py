import os
import random

from image_utils import process_image
from shared import init_single_dir, map_files, read_text_file, sample_files
from tqdm import tqdm

DATASET_NAME = "NIH_xr_chest"
CLASS_NAME = "xr_chest"
SUFFIX = "_NIH"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = DATASET_DIR

TRAIN_FILE = os.path.join(DATASET_DIR, "train_val_list.txt")
VAL_FILE = os.path.join(DATASET_DIR, "test_list.txt")

N_TRAIN = 5000
N_VAL = 500


def process_files(filenames, dst_dir, file_map, tqdm_desc="Processing files"):
    for f in tqdm(filenames, desc=tqdm_desc):
        if f in file_map:
            process_image(file_map[f], dst_dir)


def main():
    random.seed(42)

    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)
    train_files = sample_files(read_text_file(TRAIN_FILE), N_TRAIN)
    val_files = sample_files(read_text_file(VAL_FILE), N_VAL)
    file_map = map_files(SRC_DIR)

    process_files(train_files, train_dst, file_map, "Processing train files")
    process_files(val_files, val_dst, file_map, "Processing val files")


if __name__ == "__main__":
    main()
