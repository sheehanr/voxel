from collections import defaultdict
from pathlib import Path

import pandas as pd
from tqdm import tqdm
from scripts.preprocessing.utils import init_multi_dirs, process_image

DATASET_NAME = "xr_upper_AIMI"
SUFFIX = "_AIMI"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR / "MURA-v1.1"

TRAIN_CSV = SRC_DIR / "train_image_paths.csv"
VAL_CSV = SRC_DIR / "valid_image_paths.csv"

CLASS_MAP = {
    "XR_ELBOW": "xr_elbow",
    "XR_FINGER": "xr_finger",
    "XR_FOREARM": "xr_forearm",
    "XR_HAND": "xr_hand",
    "XR_HUMERUS": "xr_humerus",
    "XR_SHOULDER": "xr_shoulder",
    "XR_WRIST": "xr_wrist",
}


def process_row(row, class_map, dataset_dir, dst_map, class_counts):
    relative_path = row[0]
    parts = relative_path.split("/")

    raw_class_name = parts[2]
    raw_patient_id = parts[3]
    raw_study_id = parts[4]

    if raw_class_name not in class_map:
        return

    class_name = class_map[raw_class_name]
    patient_id = raw_patient_id[7:]  # patient00001 -> 00001
    study_id = f"{raw_study_id[0]}{raw_study_id[5]}{raw_study_id[7]}"  # study1_positive -> s1p

    if class_counts[class_name] >= 5000:
        return

    filepath = dataset_dir / relative_path
    dst_dir = dst_map[class_name]

    prefix = f"{patient_id}_{study_id}_"
    process_image(filepath, dst_dir, prefix)

    class_counts[class_name] += 1


def process_csv(csv_path, dataset_dir, class_map, dst_map, tqdm_desc="Processing files"):
    df = pd.read_csv(csv_path, header=None)

    # for undersampling classes with over 5000 files
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    class_counts = defaultdict(int)

    for _, row in tqdm(df.iterrows(), total=len(df), desc=tqdm_desc):
        process_row(row, class_map, dataset_dir, dst_map, class_counts)


def main():
    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, VAL_DIR, "xr", SUFFIX)

    process_csv(TRAIN_CSV, DATASET_DIR, CLASS_MAP, train_dst_map, "Processing train files")
    process_csv(VAL_CSV, DATASET_DIR, CLASS_MAP, val_dst_map, "Processing val files")


if __name__ == "__main__":
    main()
