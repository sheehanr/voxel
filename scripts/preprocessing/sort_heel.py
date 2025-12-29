import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))

UNSORTED_DIR = os.path.join(DATA_DIR, "unsorted/heel_dataset")

# pytorch class directories
TRAIN_DIR = os.path.join(DATA_DIR, "train/xr_heel")
TEST_DIR = os.path.join(DATA_DIR, "test/xr_heel")

# in case class directories are not empty
BACKUP_TRAIN_DIR = os.path.join(DATA_DIR, "unsorted/heel_dataset/sorted_train")
BACKUP_TEST_DIR = os.path.join(DATA_DIR, "unsorted/heel_dataset/sorted_test")

TRAIN_SAMPLE_PERCENT = 0.9
TEST_SAMPLE_PERCENT = 0.1
TARGET_DIMENSIONS = (256, 256)


# return paths of target directories
def target_directories():
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)

    # create backups if needed
    if len(os.listdir(TRAIN_DIR)) > 0 or len(os.listdir(TEST_DIR)) > 0:
        print("ERROR: Primary train and/or test directory not empty, files will be stored in backup directories")
        os.makedirs(BACKUP_TRAIN_DIR, exist_ok=True)
        os.makedirs(BACKUP_TEST_DIR, exist_ok=True)

        return BACKUP_TRAIN_DIR, BACKUP_TEST_DIR

    return TRAIN_DIR, TEST_DIR


def main():
    pass


if __name__ == "__main__":
    main()
