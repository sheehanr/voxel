import os
import random

from image_utils import process_image
from shared import init_single_dir, map_files, sample_files
from tqdm import tqdm

DATASET_NAME = "NIH_xr_chest"
CLASS_NAME = "xr_chest"
CLASS_SUBDIR = "xr_chest_NIH"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = DATASET_DIR

TRAIN_FILE = os.path.join(DATASET_DIR, "train_val_list.txt")
VAL_FILE = os.path.join(DATASET_DIR, "test_list.txt")

TRAIN_DST = os.path.join(TRAIN_DIR, CLASS_NAME)
VAL_DST = os.path.join(VAL_DIR, CLASS_NAME)

N_TRAIN = 5000
N_VAL = 500


# return list of files in text file
def read_text_file(filepath):
    with open(filepath, "r") as f:
        filenames = [line.strip() for line in f.readlines()]

    return filenames


def main():
    random.seed(42)

    train_dst, val_dst = init_single_dir(CLASS_NAME, CLASS_SUBDIR, TRAIN_DST, VAL_DST)
    train_files = sample_files(read_text_file(TRAIN_FILE), N_TRAIN)
    val_files = sample_files(read_text_file(VAL_FILE), N_VAL)

    file_map = map_files(SRC_DIR)

    for filename in tqdm(train_files):
        if filename in file_map:
            filepath = file_map[filename]
            process_image(filepath, train_dst)

    for filename in tqdm(val_files):
        if filename in file_map:
            filepath = file_map[filename]
            process_image(filepath, val_dst)


if __name__ == "__main__":
    main()
