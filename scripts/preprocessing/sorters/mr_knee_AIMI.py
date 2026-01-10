from pathlib import Path

DATASET_NAME = "mr_knee_AIMI"
CLASS_NAME = "mr_knee"
SUFFIX = "_AIMI"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR / "MRNet-v1.0"


def main():
    pass


if __name__ == "__main__":
    main()
