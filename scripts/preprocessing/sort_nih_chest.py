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

    target_train_dir = SORTED_TRAIN_DIR
    target_val_dir = SORTED_VAL_DIR

    # create backups if needed
    if len(os.listdir(SORTED_TRAIN_DIR)) > 0 or len(os.listdir(SORTED_VAL_DIR)) > 0:
        print("WARNING: data/train/xr_chest or data/val/xr_chest are not empty. What would you like to do?:")
        print("\t1. Continue with placing the images in those folders")
        print("\t2. Place the images in data/[...]/xr_chest/xr_chest_NIH")
        print("\t(Note: option 2 requires manual review and transfer of files into xr_chest before training)")
        choice = input("Enter 1 or 2: ")

        if choice != "1":
            target_train_dir = os.path.join(SORTED_TRAIN_DIR, "xr_chest_NIH")
            target_val_dir = os.path.join(SORTED_VAL_DIR, "xr_chest_NIH")

            os.makedirs(target_train_dir, exist_ok=True)
            os.makedirs(target_val_dir, exist_ok=True)

    return target_train_dir, target_val_dir


# load file names from text file into a list
def load_text_file(txt_path):
    with open(txt_path, "r") as f:
        filenames = [line.strip() for line in f.readlines()]

    return filenames


# select files randomly from list
def undersample(filenames, sample_size):
    return random.sample(filenames, sample_size)


# standardize images and save to correct directory
def process_files(filenames, destination):
    for filename in tqdm(filenames):
        filepath = os.path.join(UNSORTED_DIR, filename)
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

    process_files(selected_train, target_train_dir)
    process_files(selected_val, target_val_dir)


if __name__ == "__main__":
    main()
