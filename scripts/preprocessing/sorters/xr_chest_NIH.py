import random
from pathlib import Path

from tqdm import tqdm
from scripts.preprocessing.utils import init_single_dir, map_files, process_image, read_text_file, sample_files

DATASET_NAME = "xr_chest_NIH"
CLASS_NAME = "xr_chest"
SUFFIX = "_NIH"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASET_DIR = DATA_DIR / "downloads" / DATASET_NAME
SRC_DIR = DATASET_DIR

TRAIN_FILE = DATASET_DIR / "train_val_list.txt"
VAL_FILE = DATASET_DIR / "test_list.txt"

N_TRAIN = 4140
N_VAL = 460


def process_files(filenames, dst_dir, file_map, tqdm_desc="Processing files"):
    for f in tqdm(filenames, desc=tqdm_desc):
        if f in file_map:
            process_image(file_map[f], dst_dir)


def main():
    random.seed(42)

    train_dst, val_dst = init_single_dir(CLASS_NAME, TRAIN_DIR, VAL_DIR, SUFFIX)
    train_files = sample_files(read_text_file(TRAIN_FILE), N_TRAIN)
    val_files = sample_files(read_text_file(VAL_FILE), N_VAL)
    file_map = map_files(SRC_DIR)

    process_files(train_files, train_dst, file_map, "Processing train files")
    process_files(val_files, val_dst, file_map, "Processing val files")


if __name__ == "__main__":
    main()
