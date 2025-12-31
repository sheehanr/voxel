import os
import random


# directory setup for datasets with multiple classes; no return
def multi_class_setup_directories(dir, classes_dict, subdir_suffix="", sorted_train_dir=dir):
    os.makedirs(dir, exist_ok=True)

    for val in classes_dict.values():
        subdir_name = val + subdir_suffix  # in case folder is moved into main class folders
        os.makedirs(os.path.join(sorted_train_dir, subdir_name), exist_ok=True)


# directory setup for datasets with one class; return paths of target directories
def setup_directories(pytorch_class, class_subdir, sorted_train_dir, sorted_val_dir):
    os.makedirs(sorted_train_dir, exist_ok=True)
    os.makedirs(sorted_val_dir, exist_ok=True)

    print("Where should images be placed?:")
    print(f"    1. Directly in data/train/{pytorch_class}")
    print(f"    2. In subdirectory data/train/{pytorch_class}/{class_subdir} (recommended)")
    print("    (Note: option 2 requires manual review and transfer before training)")
    choice = input("Enter 1 or 2: ")
    print("")

    if choice != "1":
        target_train_dir = os.path.join(sorted_train_dir, class_subdir)
        target_val_dir = os.path.join(sorted_val_dir, class_subdir)

        os.makedirs(target_train_dir, exist_ok=True)
        os.makedirs(target_val_dir, exist_ok=True)

        return target_train_dir, target_val_dir

    else:
        return sorted_train_dir, sorted_val_dir


def get_subdirectories(unsorted_dir):
    return [d for d in os.listdir(unsorted_dir) if os.path.isdir(os.path.join(unsorted_dir, d))]


# returns list of all image paths
def list_filepaths(unsorted_dir, subdirs_list):
    all_filepaths = []
    for subdir in subdirs_list:
        subdir_path = os.path.join(unsorted_dir, subdir)
        for filename in os.listdir(subdir_path):
            if filename.startswith("."):
                continue

            all_filepaths.append(os.path.join(subdir_path, filename))

    return all_filepaths


# randomly separate files into train and val
def split_dataset(all_filepaths, split_ratio=0.9):
    random.shuffle(all_filepaths)
    train_len = int(len(all_filepaths) * split_ratio)

    train_filepaths = all_filepaths[:train_len]
    val_filepaths = all_filepaths[train_len:]

    return train_filepaths, val_filepaths


# map each unique filename to its full path
def create_file_map(unsorted_dir, extensions=[".png", ".jpg", ".jpeg", ".dcm"]):
    file_map = {}
    for root, dir_names, filenames in os.walk(unsorted_dir):
        for f in filenames:
            if any(f.lower().endswith(ext) for ext in extensions):
                file_map[f] = os.path.join(root, f)

    return file_map


# select files randomly from list
def undersample(filenames, sample_size=5500):
    return random.sample(filenames, sample_size)
