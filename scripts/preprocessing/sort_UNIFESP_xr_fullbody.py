import os

import pandas as pd
from image_utils import load_dcm, standardize_pil
from shared import init_multi_dirs
from tqdm import tqdm

DATASET_NAME = "UNIFESP_xr_fullbody"
SUFFIX = "_UNIFESP"

# note: test folder is not included because it is unlabeled in dataset
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = os.path.join(DATASET_DIR, "train")

TRAIN_CSV = os.path.join(DATASET_DIR, "train.csv")

TRAIN_DST = os.path.join(TRAIN_DIR, "xr_UNIFESP")
MULTI_TARGET_DST = os.path.join(TRAIN_DST, "xr_multi_target")

CLASS_MAP = {
    0: "xr_abdomen",
    1: "xr_ankle",
    2: "xr_cervical_spine",
    3: "xr_chest",
    4: "xr_clavicles",
    5: "xr_elbow",
    6: "xr_foot",
    7: "xr_finger",
    8: "xr_forearm",
    9: "xr_hand",
    10: "xr_hip",
    11: "xr_knee",
    12: "xr_tibia",
    13: "xr_lumbar_spine",
    14: "xr_others",
    15: "xr_pelvis",
    16: "xr_shoulder",
    17: "xr_sinus",
    18: "xr_skull",
    19: "xr_femur",
    20: "xr_thoracic_spine",
    21: "xr_wrist",
}


# print information about data placement
def important_info():
    print("IMPORTANT INFO:")
    print("- Single target images saved in data/train/xr_UNIFESP/xr_[bodypart]_UNIFESP")
    print("- Multi target images saved in data/train/xr_UNIFESP/xr_multi_target")
    print("- Test data ignored (no labels provided)")
    print("- Manual review is required before training\n")


# get unique image id and map it to its full path
def map_files(src_dir):
    file_map = {}
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith(".dcm"):
                image_id = f.split("-")[0]  # files end in "-c" which is not part of image id
                file_map[image_id] = os.path.join(root, f)

    return file_map


def save_multi_target(img, targets, multi_target_dst, dcm_filename):
    dst_path = os.path.join(multi_target_dst, f"{'_'.join(targets)}_{dcm_filename}.png")
    img.save(dst_path)


def save_single_target(img, target, dst_map, class_map, dcm_filename):
    class_name = class_map[target]
    if class_name in dst_map:
        dst_path = os.path.join(dst_map[class_name], f"{dcm_filename}.png")
        img.save(dst_path)


# read one row of csv and process image
def process_row(row, file_map, dst_map, class_map, multi_target_dst):
    image_id = row["SOPInstanceUID"]
    if image_id not in file_map:
        return

    dcm_path = file_map[image_id]
    dcm_filename = os.path.splitext(os.path.basename(dcm_path))[0]

    img = load_dcm(dcm_path)
    if img is None:
        return
    img = standardize_pil(img)

    target_str = str(row["Target"]).strip()
    targets = target_str.split(" ")

    # save image based on amount of targets
    if len(targets) > 1:
        save_multi_target(img, targets, multi_target_dst, dcm_filename)
    else:
        save_single_target(img, int(targets[0]), dst_map, class_map, dcm_filename)


def process_csv(train_csv, file_map, dst_map, class_map, multi_target_dst):
    df = pd.read_csv(train_csv)
    os.makedirs(multi_target_dst, exist_ok=True)
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing files"):
        process_row(row, file_map, dst_map, class_map, multi_target_dst)


def main():
    important_info()

    train_dst_map, _ = init_multi_dirs(CLASS_MAP, TRAIN_DIR, None, "xr", SUFFIX, False)
    file_map = map_files(SRC_DIR)

    process_csv(TRAIN_CSV, file_map, train_dst_map, CLASS_MAP, MULTI_TARGET_DST)


if __name__ == "__main__":
    main()
