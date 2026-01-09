from collections import defaultdict
from pathlib import Path

from utils import init_multi_dirs, process_classes, read_text_file

DATASET_NAME = "xr_lower_AIMI"
SUFFIX = "_AIMI"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR

ALLOWLIST = SCRIPT_DIR / "lists/AIMI_xr_lower_allowlist.txt"

CLASS_MAP = {
    "xr_knee_AIMI": "xr_knee",
    "xr_hip_AIMI": "xr_hip",
    "xr_ankle_AIMI": "xr_ankle",
    "xr_foot_AIMI": "xr_foot",
}


def prefix_func(f):
    return f[:5]  # custom filename without extension


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


# map custom basename to the original file's path
def map_custom_filenames(src_dir, dir_lists_map, ext):
    file_map = {}  # "1023_0.png" --> "../1023/ST-1/0.png"

    for top_dir in dir_lists_map:
        patient_dir = src_dir / top_dir

        if not patient_dir.exists():
            continue

        for f in patient_dir.rglob("*"):
            if f.is_file() and f.name in dir_lists_map[top_dir]:
                if f.suffix.lower() == ext:
                    key = f"{top_dir}_{f.name}"
                    file_map[key] = f

    return file_map


def process_dataset(src_dir, allowlist, class_map, train_dst_map, val_dst_map, ext=".png"):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [process_dataset]: {src_dir} not found")
        return

    allowlist = read_text_file(allowlist)
    if allowlist is None:
        return

    class_lists_map = defaultdict(list)  # "xr_ankle" --> ["1023_0.png", "1125_0.png", ...]
    dir_lists_map = defaultdict(list)  # "1001" --> ["0.png", "1.png", ...]

    parse_allowlist(allowlist, class_map, class_lists_map, dir_lists_map)
    file_map = map_custom_filenames(src_dir, dir_lists_map, ext)
    process_classes(class_lists_map, file_map, train_dst_map, val_dst_map, prefix_func)


def main():
    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, VAL_DIR, "xr", SUFFIX)
    process_dataset(SRC_DIR, ALLOWLIST, CLASS_MAP, train_dst_map, val_dst_map)


if __name__ == "__main__":
    main()
