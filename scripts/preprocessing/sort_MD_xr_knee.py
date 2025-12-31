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


def main():
    pass


if __name__ == "__main__":
    main()
