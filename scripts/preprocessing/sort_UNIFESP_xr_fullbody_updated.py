import os
import random
from collections import defaultdict

from image_utils import process_image
from shared import init_multi_dirs, load_allowlist, map_files, split_data
from tqdm import tqdm

DATASET_NAME = "UNIFESP_xr_fullbody"
SUFFIX = "_UNIFESP"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = os.path.join(DATASET_DIR, "train")

ALLOWLIST = os.path.join(SCRIPT_DIR, "lists/UNIFESP_allowlist.txt")

CLASS_MAP = {
    "xr_abdomen_UNIFESP": "xr_other",
    "xr_ankle_UNIFESP": "xr_ankle",
    "xr_cervical_spine_UNIFESP": "xr_other",
    "xr_chest_frontal_UNIFESP": "xr_chest",
    "xr_chest_lateral_UNIFESP": "xr_chest",
    "xr_elbow_UNIFESP": "xr_elbow",
    "xr_femur_UNIFESP": "xr_other",
    "xr_foot_UNIFESP": "xr_foot",
    "xr_forearm_UNIFESP": "xr_forearm",
    "xr_hand_UNIFESP": "xr_hand",
    "xr_hip_UNIFESP": "xr_hip",
    "xr_knee_UNIFESP": "xr_knee",
    "xr_lumbar_spine_UNIFESP": "xr_other",
    "xr_pelvis_UNIFESP": "xr_other",
    "xr_shoulder_UNIFESP": "xr_shoulder",
    "xr_skull_UNIFESP": "xr_other",
    "xr_tibia_UNIFESP": "xr_other",
    "xr_wrist_UNIFESP": "xr_wrist",
}


def process_class(class_name, file_list, file_map, dst_map, pbar):
    for f in file_list:
        if f in file_map:
            process_image(file_map[f], dst_map[class_name])
            pbar.update(1)


def process_files(class_lists, file_map, train_dst_map, val_dst_map):
    total_files = sum(len(files) for files in class_lists.values())
    with tqdm(total=total_files, desc="Processing files") as pbar:
        for class_name, file_list in class_lists.items():
            train_files, val_files = split_data(file_list)

            process_class(class_name, train_files, file_map, train_dst_map, pbar)
            process_class(class_name, val_files, file_map, val_dst_map, pbar)


def change_extension(basename, new_ext):
    filename = os.path.splitext(basename)[0]
    if new_ext[0] != ".":
        new_ext = f".{new_ext}"

    return f"{filename}{new_ext}"


def parse_allowlist(allowlist, class_map, class_lists):
    chest_frontal_count = 0

    for row in allowlist:
        parts = row.split("/")
        raw_class_name = parts[1]
        raw_filename = parts[2]

        if raw_class_name not in class_map:
            continue

        if raw_class_name == "xr_chest_frontal_UNIFESP":
            if chest_frontal_count >= 218:
                continue
            chest_frontal_count += 1

        class_name = class_map[raw_class_name]
        filename = change_extension(raw_filename, ".dcm")

        class_lists[class_name].append(filename)


def process_dataset(src_dir, allowlist, class_map, train_dst_map, val_dst_map):
    file_map = map_files(src_dir)
    allowlist = load_allowlist(allowlist)
    if allowlist is None:
        return

    random.shuffle(allowlist)
    class_lists = defaultdict(list)

    parse_allowlist(allowlist, class_map, class_lists)
    process_files(class_lists, file_map, train_dst_map, val_dst_map)


def main():
    random.seed(42)

    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, VAL_DIR, "xr", SUFFIX)
    process_dataset(SRC_DIR, ALLOWLIST, CLASS_MAP, train_dst_map, val_dst_map)


if __name__ == "__main__":
    main()
