import os
import random


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
    if single_dst_prompt(class_name, suffix) != "1":
        class_subdir = f"{class_name}{suffix}"
        train_dst = os.path.join(train_dir, class_subdir)
        val_dst = os.path.join(val_dir, class_subdir)

    train_dst = os.path.join(train_dir, class_name)
    val_dst = os.path.join(val_dir, class_name)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

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
def init_multi_dirs(class_map, train_dir, val_dir=None, modality="", suffix=""):
    train_dst_map = {}
    val_dst_map = {}

    choice = multi_dst_prompt(modality, suffix)

    for class_name in class_map.values():
        if choice == "1":
            sub_path = class_name
        elif choice == "2":
            sub_path = os.path.join(class_name, f"{class_name}{suffix}")
        else:
            sub_path = os.path.join(f"{modality}{suffix}", f"{class_name}{suffix}")

        # create train dir
        train_dst = os.path.join(train_dir, sub_path)
        os.makedirs(train_dst, exist_ok=True)
        train_dst_map[class_name] = train_dst

        # create train dir if needed
        if val_dir is not None:
            val_dst = os.path.join(val_dir, sub_path)
            os.makedirs(val_dst, exist_ok=True)
            val_dst_map[class_name] = val_dst

    return train_dst_map, val_dst_map


# return list of files in text file
def read_text_file(filepath):
    if not os.path.exists(filepath):
        print(f"ERROR [read_text_file]: {filepath} not found")
        return []

    with open(filepath, "r") as f:
        filenames = [line.strip() for line in f.readlines()]

    return filenames


# map each unique filename to its full path
def map_files(src_dir, exts=[".png", ".jpg", ".jpeg", ".dcm"]):
    if not os.path.exists(src_dir):
        print(f"ERROR [map_files]: {src_dir} not found")
        return {}

    file_map = {}

    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if any(f.lower().endswith(ext) for ext in exts):
                file_map[f] = os.path.join(root, f)

    return file_map


# return list of subdirectories of given directory
def get_subdirs(src_dir):
    if not os.path.exists(src_dir):
        print(f"ERROR [get_subdirs]: {src_dir} not found")
        return []

    return [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]


# return list of all filepaths from all subdirectories in a given directory
def get_filepaths(src_dir, subdirs):
    if not os.path.exists(src_dir):
        print(f"ERROR [get_filepaths]: {src_dir} not found")
        return []

    file_list = []

    for subdir in subdirs:
        subdir_path = os.path.join(src_dir, subdir)
        for filename in os.listdir(subdir_path):
            if filename.startswith("."):
                continue

            file_list.append(os.path.join(subdir_path, filename))

    return file_list


# randomly separate files into train and val
def split_data(file_list, split_ratio=0.9):
    random.shuffle(file_list)
    n_train = int(len(file_list) * split_ratio)

    train_files = file_list[:n_train]
    val_files = file_list[n_train:]

    return train_files, val_files


# select randomly from list of filenames (not full path)
def sample_files(filenames, n=5500):
    return random.sample(filenames, n)
