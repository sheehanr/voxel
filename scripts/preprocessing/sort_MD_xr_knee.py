import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads/MD_xr_knee")
UNSORTED_DIR = os.path.join(
    DATASET_DIR,
    "Digital Knee X-ray Images",
    "Digital Knee X-ray Images",
    "Knee X-ray Images",
    "MedicalExpert-I",  # MedicalExpert-I and MedicalExpert-II have the same images
    "MedicalExpert-I",
)

# pytorch class directories
SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, "xr_knee")
SORTED_VAL_DIR = os.path.join(VAL_DIR, "xr_knee")

TRAIN_SAMPLE_PERCENT = 0.9
TARGET_DIMENSIONS = (256, 256)


# return paths of target directories
def setup_directories():
    os.makedirs(SORTED_TRAIN_DIR, exist_ok=True)
    os.makedirs(SORTED_VAL_DIR, exist_ok=True)

    print("Where should images be placed?:")
    print("\t1. Directly in data/train/xr_knee")
    print("\t2. In subfolder data/train/xr_knee/xr_knee_MD (requires manual review and transfer before training)")
    choice = input("Enter 1 or 2: ")

    if choice != "1":
        target_train_dir = os.path.join(SORTED_TRAIN_DIR, "xr_knee_MD")
        target_val_dir = os.path.join(SORTED_VAL_DIR, "xr_knee_MD")

        os.makedirs(target_train_dir, exist_ok=True)
        os.makedirs(target_val_dir, exist_ok=True)

        return target_train_dir, target_val_dir
    else:
        return SORTED_TRAIN_DIR, SORTED_VAL_DIR


def main():
    pass


if __name__ == "__main__":
    main()
