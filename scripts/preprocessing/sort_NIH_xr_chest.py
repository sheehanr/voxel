import os
import random

from converters import standardize_image
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads/NIH_xr_chest")

# pytorch class names
SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, "xr_chest")
SORTED_VAL_DIR = os.path.join(VAL_DIR, "xr_chest")

TRAIN_FILE = os.path.join(DATASET_DIR, "train_val_list.txt")
VAL_FILE = os.path.join(DATASET_DIR, "test_list.txt")

TRAIN_SAMPLE_SIZE = 5000
VAL_SAMPLE_SIZE = 500
TARGET_DIMENSIONS = (256, 256)


# return paths of target directories
def setup_directories():
    os.makedirs(SORTED_TRAIN_DIR, exist_ok=True)
    os.makedirs(SORTED_VAL_DIR, exist_ok=True)

    print("Where should images be placed?:")
    print("    1. Directly in data/train/xr_chest")
    print("    2. In subfolder data/train/xr_knee/xr_knee_MD (recommended)")
    print("    (Note: option 2 requires manual review and transfer before training)")
    choice = input("Enter 1 or 2: ")
    print("")

    if choice != "1":
        target_train_dir = os.path.join(SORTED_TRAIN_DIR, "xr_chest_NIH")
        target_val_dir = os.path.join(SORTED_VAL_DIR, "xr_chest_NIH")

        os.makedirs(target_train_dir, exist_ok=True)
        os.makedirs(target_val_dir, exist_ok=True)

        return target_train_dir, target_val_dir
    else:
        return SORTED_TRAIN_DIR, SORTED_VAL_DIR


# load file names from text file into a list
def load_text_file(txt_path):
    with open(txt_path, "r") as f:
        filenames = [line.strip() for line in f.readlines()]

    return filenames


# select files randomly from list
def undersample(filenames, sample_size):
    return random.sample(filenames, sample_size)


# map each unique filename to its full path
def create_file_map():
    file_map = {}
    for root, dir_names, filenames in os.walk(DATASET_DIR):
        for f in filenames:
            if f.endswith(".png"):
                file_map[f] = os.path.join(root, f)

    return file_map


# standardize images and save to correct directory
def process_files(filenames, destination, file_map):
    for filename in tqdm(filenames):
        if filename not in file_map:
            continue

        filepath = file_map[filename]
        if not os.path.exists(filepath):
            continue

        img = standardize_image(filepath, TARGET_DIMENSIONS)
        save_path = os.path.join(destination, filename)

        img.save(save_path)


def main():
    random.seed(42)

    target_train_dir, target_val_dir = setup_directories()
    selected_train = undersample(load_text_file(TRAIN_FILE), TRAIN_SAMPLE_SIZE)
    selected_val = undersample(load_text_file(VAL_FILE), VAL_SAMPLE_SIZE)

    file_map = create_file_map()

    process_files(selected_train, target_train_dir, file_map)
    process_files(selected_val, target_val_dir, file_map)


if __name__ == "__main__":
    main()
