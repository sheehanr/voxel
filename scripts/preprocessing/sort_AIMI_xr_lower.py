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
def process_csv(csv_path, allowed_set):
    df = pd.read_csv(csv_path, header=None)

    pbar_total = len(allowed_set) if allowed_set else 1297
    with tqdm(total=pbar_total, desc="Processing files") as pbar:
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

                    if allowed_set is not None:
                        candidate_name = f"{current_dir}_{os.path.splitext(f)[0]}.png"
                        if candidate_name not in allowed_set:
                            continue

                    filepath = os.path.join(root, f)
                    dst_subdir = class_name + SUFFIX
                    dst_dir = os.path.join(TRAIN_DST, dst_subdir)

                    prefix = current_dir + "_"
                    process_image(filepath, dst_dir, prefix)

                    pbar.update(1)


def load_allowlist(allowlist_path):
    if not os.path.exists(allowlist_path):
        print(f"ERROR [load_allowlist]: {allowlist_path} not found")
        return None

    raw_list = read_text_file(allowlist_path)
    return set(os.path.basename(f) for f in raw_list)


def main():
    print("IMPORTANT NOTES:")
    print(f"- All files will be saved in data/train/xr_AIMI/xr_[bodypart]{SUFFIX}")
    print("- Manual review and transfer is required before training\n")

    init_multi_dirs(CLASS_MAP, TRAIN_DST, None, SUFFIX)
    allowed_set = load_allowlist(ALLOWLIST)

    if allowed_set is None:
        print("WARNING: allowlist not found. All files, including duplicates, will be saved.")
        confirm = input("Continue? (y/n): ")
        print("")
        if confirm.lower() != "y":
            return

    process_csv(TRAIN_CSV, allowed_set)


if __name__ == "__main__":
    main()
