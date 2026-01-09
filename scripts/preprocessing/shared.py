import random
from pathlib import Path

from image_utils import process_image
from tqdm import tqdm


# directory setup prompt for datasets with one class
def single_dst_prompt(class_name, suffix):
    print(f"\nSelect destination for '{class_name}' dataset:")
    print(f"  [1] MERGE: data/train/{class_name}")
    print(f"  [2] REVIEW IN CLASS: data/train/{class_name}/{class_name}{suffix}")

    choice = input("\nChoice (1/2): ").strip()
    print("")
    return choice


# directory setup for datasets with one class; return paths of target directories
def init_single_dir(class_name, train_dir, val_dir, suffix=""):
    train_dir = Path(train_dir)
    val_dir = Path(val_dir)

    choice = single_dst_prompt(class_name, suffix)

    if choice == "1":
        sub_path = Path(class_name)
    else:
        sub_path = Path(class_name) / f"{class_name}{suffix}"

    train_dst = train_dir / sub_path
    train_dst.mkdir(parents=True, exist_ok=True)

    val_dst = val_dir / sub_path
    val_dst.mkdir(parents=True, exist_ok=True)

    return train_dst, val_dst


# directory setup prompt for datasets with multiple classes
def multi_dst_prompt(modality, suffix):
    print(f"\nSelect destination for ALL '{modality}_*' classes:")
    print(f"  [1] MERGE: data/train/{modality}_[class]")
    print(f"  [2] REVIEW IN CLASS: data/train/{modality}_[class]/{modality}_[class]{suffix}")
    print(f"  [3] REVIEW IN DATASET: data/train/{modality}{suffix}/{modality}_[class]{suffix}")

    choice = input("\nChoice (1/2/3): ").strip()
    print("")
    return choice


# directory setup for datasets with multiple classes; return maps of target directories
def init_multi_dirs(class_map, train_dir, val_dir=None, modality="", suffix="", prompt=True):
    train_dir = Path(train_dir)

    train_dst_map = {}
    val_dst_map = {}

    if prompt:
        choice = multi_dst_prompt(modality, suffix)
    else:
        choice = "3"

    for class_name in class_map.values():
        if choice == "1":
            sub_path = Path(class_name)
        elif choice == "2":
            sub_path = Path(class_name) / f"{class_name}{suffix}"
        else:
            sub_path = Path(f"{modality}{suffix}") / f"{class_name}{suffix}"

        # create train dir
        train_dst = train_dir / sub_path
        train_dst.mkdir(parents=True, exist_ok=True)
        train_dst_map[class_name] = train_dst

        # create train dir if needed
        if val_dir is not None:
            val_dir = Path(val_dir)

            val_dst = val_dir / sub_path
            val_dst.mkdir(parents=True, exist_ok=True)
            val_dst_map[class_name] = val_dst

    return train_dst_map, val_dst_map


# return list of files in text file
def read_text_file(filepath):
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"ERROR [read_text_file]: {filepath} not found")
        return []

    with open(filepath, "r") as f:
        file_list = [line.strip() for line in f.readlines()]

    return file_list


# map each unique filename to its full path
def map_files(src_dir, exts=[".png", ".jpg", ".jpeg", ".dcm"]):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [map_files]: {src_dir} not found")
        return {}

    file_map = {}

    for f in src_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in exts:
            file_map[f.name] = f

    return file_map


# return list of subdirectories of given directory
def get_subdirs(src_dir):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [get_subdirs]: {src_dir} not found")
        return []

    subdirs = []

    for d in src_dir.iterdir():
        if d.is_dir():
            subdirs.append(d.name)

    return subdirs


# return list of all filepaths from all subdirectories in a given directory
def get_filepaths(src_dir, subdirs):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [get_filepaths]: {src_dir} not found")
        return []

    filepaths = []

    for subdir in subdirs:
        subdir_path = src_dir / subdir
        for f in subdir_path.iterdir():
            if f.is_file() and not f.name.startswith("."):
                filepaths.append(f)

    return filepaths


# randomly separate files into train and val
def split_data(file_list, split_ratio=0.9):
    random.shuffle(file_list)
    n_train = int(len(file_list) * split_ratio)

    train_files = file_list[:n_train]
    val_files = file_list[n_train:]

    return train_files, val_files


# randomly select files from list
def sample_files(file_list, n=5500):
    return random.sample(file_list, n)


def process_class_files(class_name, file_list, file_map, dst_map, prefix_func, custom_name_func, pbar):
    for f in file_list:
        if f in file_map:
            filepath = file_map[f]
            prefix, custom_name = None, None

            if prefix_func:
                prefix = prefix_func(f)
            if custom_name_func:
                custom_name = custom_name_func(filepath)

            process_image(filepath, dst_map[class_name], prefix, custom_name)
            pbar.update(1)


def process_classes(class_lists_map, file_map, train_dst_map, val_dst_map, prefix_func=None, custom_name_func=None):
    total_files = sum(len(files) for files in class_lists_map.values())
    with tqdm(total=total_files, desc="Processing files") as pbar:
        for class_name, file_list in class_lists_map.items():
            train_files, val_files = split_data(file_list)

            process_class_files(class_name, train_files, file_map, train_dst_map, prefix_func, custom_name_func, pbar)
            process_class_files(class_name, val_files, file_map, val_dst_map, prefix_func, custom_name_func, pbar)
