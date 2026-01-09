from pathlib import Path


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
