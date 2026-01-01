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
    6: "xr_feet",
    7: "xr_finger",
    8: "xr_forearm",
    9: "xr_hand",
    10: "xr_hip",
    11: "xr_knee",
    12: "xr_lower_leg",
    13: "xr_lumbar_spine",
    14: "xr_others",
    15: "xr_pelvis",
    16: "xr_shoulder",
    17: "xr_sinus",
    18: "xr_skull",
    19: "xr_thigh",
    20: "xr_thoracic_spine",
    21: "xr_wrist",
}


# get unique image id and map it to its full path
def map_files():
    file_map = {}
    for root, dirs, files in os.walk(SRC_DIR):
        for f in files:
            if f.endswith(".dcm"):
                image_id = f.split("-")[0]  # files end in "-c" which is not part of image id
                file_map[image_id] = os.path.join(root, f)

    return file_map


# move images to named folders
def process_images(file_map):
    csv_df = pd.read_csv(TRAIN_CSV)
    for _, row in tqdm(csv_df.iterrows(), total=len(csv_df)):
        # verify file existence and get path
        image_id = row["SOPInstanceUID"]
        short_id = image_id[26:]  # all files have same prefix
        if image_id not in file_map:
            continue

        filepath = file_map[image_id]

        # convert and verify proper image
        img = load_dcm(filepath)
        img = standardize_pil(img)
        if img is None:
            continue

        # save image as png based on number of targets
        target_str = str(row["Target"]).strip()
        targets = target_str.split(" ")

        if len(targets) > 1:  # multiple anatomical regions
            dst_path = os.path.join(MULTI_TARGET_DST, f"{'_'.join(targets)}_{short_id}.png")
            img.save(dst_path)

        else:
            target = int(targets[0])
            dst_dir = CLASS_MAP[target] + SUFFIX
            dst_path = os.path.join(TRAIN_DST, dst_dir, f"{short_id}.png")
            img.save(dst_path)


def main():
    print("IMPORTANT NOTES:")
    print("- All files will be saved in data/train/xr_UNIFESP/xr_[bodypart]")
    print("- Images with multiple targets will be placed in .../xr_UNIFESP/xr_multi_target")
    print("- There is no file or labeling for the test folder so it will be discarded")
    print("- Manual review and transfer is required before training\n")

    init_multi_dirs([MULTI_TARGET_DST], CLASS_MAP, TRAIN_DST, None, SUFFIX)
    file_map = map_files()

    process_images(file_map)


if __name__ == "__main__":
    main()
