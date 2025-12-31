import os

DATASET_NAME = "AIMI_xr_lower"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)

SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, "xr_lower_AIMI")

CSV_FILE = os.path.join(DATASET_DIR, "labels.csv")

PYTORCH_CLASSES = {
    "XR KNEE": "xr_knee",
    "XR HIP": "xr_hip",
    "XR ANKLE": "xr_ankle",
    "XR FOOT": "xr_foot",
}


def main():
    pass


if __name__ == "__main__":
    main()
