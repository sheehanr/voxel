import os

from shared import init_multi_dirs

DATASET_NAME = "AIMI_xr_upper"
SUFFIX = "_AIMI"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = os.path.join(DATASET_DIR, "MURA-v1.1")

TRAIN_CSV = os.path.join(SRC_DIR, "train_image_paths.csv")
VAL_CSV = os.path.join(SRC_DIR, "valid_image_paths.csv")

CLASS_MAP = {
    "XR_ELBOW": "xr_elbow",
    "XR_FINGER": "xr_finger",
    "XR_FOREARM": "xr_forearm",
    "XR_HAND": "xr_hand",
    "XR_HUMERUS": "xr_humerus",
    "XR_SHOULDER": "xr_shoulder",
    "XR_WRIST": "xr_wrist",
}


def main():
    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, None, "xr", SUFFIX)


if __name__ == "__main__":
    main()
