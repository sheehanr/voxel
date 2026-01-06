import os
import random
from collections import defaultdict

from image_utils import process_image
from shared import init_multi_dirs, read_text_file, split_data
from tqdm import tqdm

DATASET_NAME = "AIMI_xr_lower"
SUFFIX = "_AIMI"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = DATASET_DIR

ALLOWLIST = os.path.join(SCRIPT_DIR, "lists/AIMI_xr_lower_allowlist.txt")

CLASS_MAP = {
    "xr_knee_AIMI": "xr_knee",
    "xr_hip_AIMI": "xr_hip",
    "xr_ankle_AIMI": "xr_ankle",
    "xr_foot_AIMI": "xr_foot",
}


def process_class(class_name, file_list, file_map, dst_map, pbar):
    for f in file_list:
        if f in file_map:
            prefix = f[:5]
            process_image(file_map[f], dst_map[class_name], prefix)
            pbar.update(1)


def process_files(class_lists_map, file_map, train_dst_map, val_dst_map):
    total_files = sum(len(files) for files in class_lists_map.values())
    with tqdm(total=total_files, desc="Processing files") as pbar:
        for class_name, file_list in class_lists_map.items():
            train_files, val_files = split_data(file_list)

            process_class(class_name, train_files, file_map, train_dst_map, pbar)
            process_class(class_name, val_files, file_map, val_dst_map, pbar)


def parse_allowlist(allowlist, class_map, class_lists_map, dir_lists_map):
    for row in allowlist:
        # map class name to list of allowed files in the class
        path_parts = row.split("/")
        raw_class_name = path_parts[1]
        raw_filename = path_parts[2]

        if raw_class_name not in class_map:
            continue

        class_name = class_map[raw_class_name]
        class_lists_map[class_name].append(raw_filename)

        # map original directory name to list of allowed files in the directory
        basename_parts = raw_filename.split("_")
        original_dir_name = basename_parts[0]
        original_basename = basename_parts[1]

        dir_lists_map[original_dir_name].append(original_basename)


def process_dataset(src_dir, allowlist, class_map, train_dst_map, val_dst_map, ext=".png"):
    if not os.path.exists(src_dir):
        print(f"ERROR [map_custom_filenames]: {src_dir} not found")
        return

    allowlist = read_text_file(allowlist)
    if allowlist is None:
        return

    random.shuffle(allowlist)
    class_lists_map = defaultdict(list)  # xr_ankle -> [1023_0.png, 1125_0.png, ...]
    dir_lists_map = defaultdict(list)  # 1001 -> [0.png, 1.png, ...]

    parse_allowlist(allowlist, class_map, class_lists_map, dir_lists_map)
    file_map = map_custom_filenames(src_dir, dir_lists_map, ext)
    process_files(class_lists_map, file_map, train_dst_map, val_dst_map)


# map custom basename to the original file's path
def map_custom_filenames(src_dir, dir_lists_map, ext):
    file_map = {}  # 1023_0.png -> ../1023/ST-1/0.png

    for root, dirs, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        top_dir = relative_path.split("/")[0]

        if top_dir in dir_lists_map:
            for f in dir_lists_map[top_dir]:
                if f in files:
                    if f.lower().endswith(ext):
                        file_map[f"{top_dir}_{f}"] = os.path.join(root, f)

    return file_map


def main():
    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, VAL_DIR, "xr", SUFFIX)
    process_dataset(SRC_DIR, ALLOWLIST, CLASS_MAP, train_dst_map, val_dst_map)


if __name__ == "__main__":
    main()
