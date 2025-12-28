import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))

UNSORTED_DIR = os.path.join(DATA_DIR, "unsorted/nih_chest/images")
TRAIN_DIR = os.path.join(DATA_DIR, "unsorted/nih_chest/sorted_train")
TEST_DIR = os.path.join(DATA_DIR, "unsorted/nih_chest/sorted_test")
TRAIN_FILE = os.path.join(DATA_DIR, "unsorted/nih_chest/train_val_list.txt")
TEST_FILE = os.path.join(DATA_DIR, "unsorted/nih_chest/test_list.txt")

TRAIN_SAMPLE_SIZE = 5000
TEST_SAMPLE_SIZE = 500
TARGET_DIMENSIONS = (256, 256)


# creates needed dirs if not created
def create_dirs():
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)


# loads text files into a list
def load_text_file(path):
    with open(path, "r") as f:
        file_contents = [line.strip() for line in f.readlines()]

    return file_contents


# selects files randomly from list
def undersample(file_contents, sample_size):
    return random.sample(file_contents, sample_size)


def main():
    random.seed(42)  # ensure same files are selected on each run
    create_dirs()


if __name__ == "__main__":
    main()
