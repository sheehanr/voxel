import random
from collections import defaultdict
from pathlib import Path

from scripts.preprocessing.utils import init_multi_dirs, map_files, process_classes, read_text_file

DATASET_NAME = "xr_fullbody_UNIFESP"
SUFFIX = "_UNIFESP"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR / "train"

ALLOWLIST = SCRIPT_DIR / "lists/UNIFESP_allowlist.txt"

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


def custom_name_func(filepath):
    filepath = Path(filepath)
    return filepath.stem[26:-2]  # all files have identical prefix and suffix


def change_extension(basename, new_ext):
    return str(Path(basename).with_suffix(new_ext))


# map class name to list of allowed files in the class
def parse_allowlist(allowlist, class_map, class_lists_map):
    chest_frontal_count = 0

    for row in allowlist:
        parts = row.split("/")
        raw_class_name = parts[1]
        raw_filename = parts[2]

        if raw_class_name not in class_map:
            continue

        if raw_class_name == "xr_chest_frontal_UNIFESP":
            if chest_frontal_count >= 218:  # 218 frontal + 182 lateral chest x-rays
                continue
            chest_frontal_count += 1

        class_name = class_map[raw_class_name]
        filename = change_extension(raw_filename, ".dcm")  # to mimic original file

        class_lists_map[class_name].append(filename)


def process_dataset(src_dir, allowlist, class_map, train_dst_map, val_dst_map):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [process_dataset]: {src_dir} not found")
        return

    allowlist = read_text_file(allowlist)
    if allowlist is None:
        return

    random.shuffle(allowlist)
    class_lists_map = defaultdict(list)

    parse_allowlist(allowlist, class_map, class_lists_map)
    file_map = map_files(src_dir)
    process_classes(class_lists_map, file_map, train_dst_map, val_dst_map, None, custom_name_func)


def main():
    random.seed(42)

    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, VAL_DIR, "xr", SUFFIX)
    process_dataset(SRC_DIR, ALLOWLIST, CLASS_MAP, train_dst_map, val_dst_map)


if __name__ == "__main__":
    main()
