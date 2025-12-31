import os
import random

from image_utils import process_image
from shared import create_file_map, setup_directories, undersample
from tqdm import tqdm

DATASET_NAME = "NIH_xr_chest"
PYTORCH_CLASS = "xr_chest"
CLASS_SUBDIR = "xr_chest_NIH"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)

SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, PYTORCH_CLASS)
SORTED_VAL_DIR = os.path.join(VAL_DIR, PYTORCH_CLASS)

TRAIN_FILE = os.path.join(DATASET_DIR, "train_val_list.txt")
VAL_FILE = os.path.join(DATASET_DIR, "test_list.txt")

TRAIN_SAMPLE_SIZE = 5000
VAL_SAMPLE_SIZE = 500


# load file names from text file into a list
def load_text_file(txt_path):
    with open(txt_path, "r") as f:
        filenames = [line.strip() for line in f.readlines()]

    return filenames


def main():
    random.seed(42)

    target_train_dir, target_val_dir = setup_directories(PYTORCH_CLASS, CLASS_SUBDIR, SORTED_TRAIN_DIR, SORTED_VAL_DIR)
    selected_train = undersample(load_text_file(TRAIN_FILE), TRAIN_SAMPLE_SIZE)
    selected_val = undersample(load_text_file(VAL_FILE), VAL_SAMPLE_SIZE)

    file_map = create_file_map(DATASET_DIR)

    for filename in tqdm(selected_train):
        if filename in file_map:
            filepath = file_map[filename]
            process_image(filepath, target_train_dir)

    for filename in tqdm(selected_val):
        if filename in file_map:
            filepath = file_map[filename]
            process_image(filepath, target_val_dir)


if __name__ == "__main__":
    main()
