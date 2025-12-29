import os
import random

from converters import standardize_image
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))

UNSORTED_DIR = os.path.join(DATA_DIR, "unsorted/nih_chest/images")
TRAIN_FILE = os.path.join(DATA_DIR, "unsorted/nih_chest/train_val_list.txt")
TEST_FILE = os.path.join(DATA_DIR, "unsorted/nih_chest/test_list.txt")

# pytorch class directories
TRAIN_DIR = os.path.join(DATA_DIR, "train/xr_chest")
TEST_DIR = os.path.join(DATA_DIR, "test/xr_chest")

# in case class directories are not empty
BACKUP_TRAIN_DIR = os.path.join(DATA_DIR, "unsorted/nih_chest/sorted_train")
BACKUP_TEST_DIR = os.path.join(DATA_DIR, "unsorted/nih_chest/sorted_test")

TRAIN_SAMPLE_SIZE = 5000
TEST_SAMPLE_SIZE = 500
TARGET_DIMENSIONS = (256, 256)


# create needed dirs if not already created
def create_dirs():
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)

    # create backups if needed
    if len(os.listdir(TRAIN_DIR)) > 0 or len(os.listdir(TEST_DIR)) > 0:
        print("ERROR: Primary train and/or test directory not empty, files will be stored in backup directories")
        os.makedirs(BACKUP_TRAIN_DIR, exist_ok=True)
        os.makedirs(BACKUP_TEST_DIR, exist_ok=True)

        return BACKUP_TRAIN_DIR, BACKUP_TEST_DIR

    return TRAIN_DIR, TEST_DIR


# loads text files into a list
def load_text_file(path):
    with open(path, "r") as f:
        file_contents = [line.strip() for line in f.readlines()]

    return file_contents


# select files randomly from list
def undersample(file_contents, sample_size):
    return random.sample(file_contents, sample_size)


# sort selected images into correct folders
def sort_imgs(file_contents, destination):
    for file in tqdm(file_contents):
        img_path = os.path.join(UNSORTED_DIR, file)
        if not os.path.exists(img_path):
            continue

        img = standardize_image(img_path, TARGET_DIMENSIONS)
        save_path = os.path.join(destination, file)
        img.save(save_path)


def main():
    random.seed(42)  # ensure same files are selected on each run
    target_train_dir, target_test_dir = create_dirs()

    selected_train = undersample(load_text_file(TRAIN_FILE), TRAIN_SAMPLE_SIZE)
    selected_test = undersample(load_text_file(TEST_FILE), TEST_SAMPLE_SIZE)

    sort_imgs(selected_train, target_train_dir)
    sort_imgs(selected_test, target_test_dir)


if __name__ == "__main__":
    main()
