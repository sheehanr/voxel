import os
import random


# directory setup for datasets with multiple classes; no return
def init_multi_dirs(dirs_to_create, class_map, train_dst, val_dst=None, suffix=""):
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)

    # create subdirectory for each class
    for val in class_map.values():
        subdir_name = val + suffix  # in case folder is moved into main class folders
        os.makedirs(os.path.join(train_dst, subdir_name), exist_ok=True)

    if val_dst is not None:  # for datasets with test/val files and labels
        for val in class_map.values():
            subdir_name = val + suffix
            os.makedirs(os.path.join(val_dst, subdir_name), exist_ok=True)


# directory setup for datasets with one class; return paths of target directories
def init_single_dir(class_name, class_subdir, train_dst, val_dst):
    os.makedirs(train_dst, exist_ok=True)
    os.makedirs(val_dst, exist_ok=True)

    print("Where should images be placed?:")
    print(f"    1. Directly in data/train/{class_name}")
    print(
        f"    2. In subdirectory data/train/{class_name}/{class_subdir} (recommended)"
    )
    print("    (Note: option 2 requires manual review and transfer before training)")
    choice = input("Enter 1 or 2: ")
    print("")

    if choice != "1":
        backup_train = os.path.join(train_dst, class_subdir)
        backup_val = os.path.join(val_dst, class_subdir)

        os.makedirs(backup_train, exist_ok=True)
        os.makedirs(backup_val, exist_ok=True)

        return backup_train, backup_val

    else:
        return train_dst, val_dst


# return list of subdirectories of given directory (to use in get_filepaths)
def get_subdirs(src_dir):
    return [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]


# return list of all filepaths from all subdirectories in a given directory
def get_filepaths(src_dir, subdirs):
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


# map each unique filename to its full path
def map_files(src_dir, exts=[".png", ".jpg", ".jpeg", ".dcm"]):
    file_map = {}
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if any(f.lower().endswith(ext) for ext in exts):
                file_map[f] = os.path.join(root, f)

    return file_map


# select randomly from list of filenames (not full path)
def sample_files(filenames, n=5500):
    return random.sample(filenames, n)


# return list of files in text file
def read_text_file(filepath):
    with open(filepath, "r") as f:
        filenames = [line.strip() for line in f.readlines()]

    return filenames
