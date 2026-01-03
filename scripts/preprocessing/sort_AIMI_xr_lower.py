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

CLASS_MAP = {
    "XR KNEE": "xr_knee",
    "XR HIP": "xr_hip",
    "XR ANKLE": "xr_ankle",
    "XR FOOT": "xr_foot",
}


def load_allowlist(allowlist_path):
    if not os.path.exists(allowlist_path):
        print(f"ERROR [load_allowlist]: {allowlist_path} not found")
        return None

    raw_list = read_text_file(allowlist_path)
    return set(os.path.basename(f) for f in raw_list)


# loop through the directory that corresponds with the current row of csv
def process_file(filepath, current_dir, class_name, dst_map, allowed_set, pbar):
    filename = os.path.basename(filepath)
    if filename.startswith("."):
        return

    if class_name not in dst_map:
        return

    if allowed_set is not None:
        candidate_name = f"{current_dir}_{os.path.splitext(filename)[0]}.png"
        if candidate_name not in allowed_set:
            return

    dst_dir = dst_map[class_name]
    prefix = f"{current_dir}_"
    process_image(filepath, dst_dir, prefix)

    pbar.update(1)


# each row of csv contains the directory name
def process_dir(row, src_dir, class_map, dst_map, allowed_set, pbar):
    current_dir = str(row[0])
    raw_class_name = str(row[1])
    if raw_class_name not in class_map:
        return

    class_name = class_map[raw_class_name]

    current_path = os.path.join(src_dir, current_dir)
    if not os.path.exists(current_path):
        return

    for root, dirs, files in os.walk(current_path):
        for f in files:
            filepath = os.path.join(root, f)
            process_file(filepath, current_dir, class_name, dst_map, allowed_set, pbar)


def process_csv(csv_path, src_dir, class_map, dst_map, allowed_set):
    df = pd.read_csv(csv_path, header=None)

    pbar_total = len(allowed_set) if allowed_set else 1297
    with tqdm(total=pbar_total, desc="Processing files") as pbar:
        for _, row in df.iterrows():
            process_dir(row, src_dir, class_map, dst_map, allowed_set, pbar)


def main():
    train_dst_map, _ = init_multi_dirs(CLASS_MAP, TRAIN_DIR, None, "xr", SUFFIX)
    allowed_set = load_allowlist(ALLOWLIST)

    if allowed_set is None:
        print("WARNING: allowlist not found. All files, including duplicates, will be saved.")
        confirm = input("Continue? (y/n): ")
        print("")
        if confirm.lower() != "y":
            return

    process_csv(TRAIN_CSV, SRC_DIR, CLASS_MAP, train_dst_map, allowed_set)


if __name__ == "__main__":
    main()
