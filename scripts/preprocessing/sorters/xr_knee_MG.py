import random
from pathlib import Path

from tqdm import tqdm
from utils import get_filepaths, init_single_dir, process_image, split_data

DATASET_NAME = "xr_knee_MG"
CLASS_NAME = "xr_knee"
SUFFIX = "_MG"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR / "OS Collected Data"


def main():
    random.seed(42)

    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)
    subdirs = ["Normal", "Osteoporosis"]
    filepaths = get_filepaths(SRC_DIR, subdirs)
    train_files, val_files = split_data(filepaths)

    for filepath in tqdm(train_files, desc="Processing train files"):
        process_image(filepath, train_dst)

    for filepath in tqdm(val_files, desc="Processing val files"):
        process_image(filepath, val_dst)


if __name__ == "__main__":
    main()
