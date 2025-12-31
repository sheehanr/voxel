import os
import random

from converters import standardize_image
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads/OT_xr_heel")
UNSORTED_DIR = os.path.join(DATASET_DIR, "all_category/all_category")

# pytorch class directories
SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, "xr_heel")
SORTED_VAL_DIR = os.path.join(VAL_DIR, "xr_heel")

TRAIN_SAMPLE_PERCENT = 0.9
TARGET_DIMENSIONS = (256, 256)


# return paths of target directories
def setup_directories():
    os.makedirs(SORTED_TRAIN_DIR, exist_ok=True)
    os.makedirs(SORTED_VAL_DIR, exist_ok=True)

    target_train_dir = SORTED_TRAIN_DIR
    target_val_dir = SORTED_VAL_DIR

    # create backups if needed
    if len(os.listdir(SORTED_TRAIN_DIR)) > 0 or len(os.listdir(SORTED_VAL_DIR)) > 0:
        print("WARNING: data/train/xr_heel or data/val/xr_heel are not empty. What would you like to do?:")
        print("\t1. Continue with placing the images in those folders")
        print("\t2. Place the images in data/[...]/xr_heel/xr_heel_OT")
        print("\t(Note: option 2 requires manual review and transfer of files into xr_chest before training)")
        choice = input("Enter 1 or 2: ")

        if choice != "1":
            target_train_dir = os.path.join(SORTED_TRAIN_DIR, "xr_heel_OT")
            target_val_dir = os.path.join(SORTED_VAL_DIR, "xr_heel_OT")

            os.makedirs(target_train_dir, exist_ok=True)
            os.makedirs(target_val_dir, exist_ok=True)

    return target_train_dir, target_val_dir

# return list of all image paths
def list_filepaths():
    all_filepaths = []
    for subdir in ["heelspur", "normal", "sever"]:
        subdir_path = os.path.join(UNSORTED_DIR, subdir)
        for filename in os.listdir(subdir_path):
            if filename.startswith("."):
                continue

            all_filepaths.append(os.path.join(subdir_path, filename))

    return all_filepaths


# randomly separate files into train and val
def split_dataset(all_filepaths, split_ratio):
    random.shuffle(all_filepaths)
    train_len = int(len(all_filepaths) * split_ratio)

    train_filepaths = all_filepaths[:train_len]
    val_filepaths = all_filepaths[train_len:]

    return train_filepaths, val_filepaths


# standardize images and save to correct directory
def process_files(filepaths, destination):
    for filepath in tqdm(filepaths):
        if not os.path.exists(filepath):
            continue

        img = standardize_image(filepath, TARGET_DIMENSIONS)
        filename = os.path.basename(filepath)
        save_path = os.path.join(destination, filename)

        img.save(save_path)


def main():
    random.seed(42)

    target_train_dir, target_val_dir = setup_directories()
    all_filepaths = list_filepaths()
    selected_train, selected_val = split_dataset(all_filepaths, TRAIN_SAMPLE_PERCENT)

    process_files(selected_train, target_train_dir)
    process_files(selected_val, target_val_dir)


if __name__ == "__main__":
    main()
