import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))

UNSORTED_DIR = os.path.join(DATA_DIR, "unsorted/heel_dataset")

# pytorch class directories
TRAIN_DIR = os.path.join(DATA_DIR, "train/xr_heel")
VAL_DIR = os.path.join(DATA_DIR, "val/xr_heel")

# in case class directories are not empty
BACKUP_TRAIN_DIR = os.path.join(DATA_DIR, "unsorted/heel_dataset/sorted_train")
BACKUP_VAL_DIR = os.path.join(DATA_DIR, "unsorted/heel_dataset/sorted_val")

TRAIN_SAMPLE_PERCENT = 0.9
VAL_SAMPLE_PERCENT = 0.1
TARGET_DIMENSIONS = (256, 256)


# return paths of target directories
def setup_directories():
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(VAL_DIR, exist_ok=True)

    # create backups if needed
    if len(os.listdir(TRAIN_DIR)) > 0 or len(os.listdir(VAL_DIR)) > 0:
        print("ERROR: Primary train and/or val directory not empty, files will be stored in backup directories")
        os.makedirs(BACKUP_TRAIN_DIR, exist_ok=True)
        os.makedirs(BACKUP_VAL_DIR, exist_ok=True)

        return BACKUP_TRAIN_DIR, BACKUP_VAL_DIR

    return TRAIN_DIR, VAL_DIR


# return list of all image paths
def list_filepaths(start_dir):
    all_filepaths = []
    for subdir in ["heelspur", "normal", "severe"]:
        subdir_path = os.path.join(UNSORTED_DIR, subdir)
        for filename in os.listdir(subdir_path):
            if filename.startswith("."):
                continue
            all_filepaths.append(os.path.join(subdir_path, filename))

    return all_filepaths


def main():
    pass


if __name__ == "__main__":
    main()
