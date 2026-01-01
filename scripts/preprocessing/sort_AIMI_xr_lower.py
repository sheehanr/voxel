import os

import pandas as pd
from image_utils import process_image
from shared import init_multi_dirs, read_text_file
from tqdm import tqdm

DATASET_NAME = "AIMI_xr_lower"
SUFFIX = "_AIMI"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = DATASET_DIR

TRAIN_CSV = os.path.join(DATASET_DIR, "labels.csv")
ALLOWLIST = os.path.join(SCRIPT_DIR, "lists/AIMI_xr_lower_allowlist.txt")

TRAIN_DST = os.path.join(TRAIN_DIR, "xr_AIMI")

CLASS_MAP = {
    "XR KNEE": "xr_knee",
    "XR HIP": "xr_hip",
    "XR ANKLE": "xr_ankle",
    "XR FOOT": "xr_foot",
}


# read csv and move files according to label
def process_csv(csv_path):
    df = pd.read_csv(csv_path, header=None)

    with tqdm(total=1297, desc="Processing files") as pbar:
        for _, row in df.iterrows():
            current_dir = str(row[0])
            class_name = CLASS_MAP[str(row[1])]

            current_path = os.path.join(SRC_DIR, current_dir)
            if not os.path.exists(current_path):
                continue

            for root, dirs, files in os.walk(current_path):
                for f in files:
                    if f.startswith("."):
                        continue

                    filepath = os.path.join(root, f)
                    dst_subdir = class_name + SUFFIX
                    dst_dir = os.path.join(TRAIN_DST, dst_subdir)

                    prefix = current_dir + "_"
                    process_image(filepath, dst_dir, prefix)

                    pbar.update(1)


def main():
    print("IMPORTANT NOTES:")
    print("- All files will be saved in data/train/xr_AIMI/xr_[bodypart]_AIMI")
    print("- Manual review and transfer is required before training\n")

    init_multi_dirs([TRAIN_DST], CLASS_MAP, TRAIN_DST, None, SUFFIX)
    process_csv(TRAIN_CSV)


if __name__ == "__main__":
    main()
