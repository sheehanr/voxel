import os

import pandas as pd
from image_utils import dcm_to_png
from tqdm import tqdm

DATASET_NAME = "UNIFESP_xr_fullbody"

# note: test folder is not included because it is unlabeled in dataset
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
UNSORTED_TRAIN_DIR = os.path.join(DATASET_DIR, "train")

# to enable manual review
SORTED_TRAIN_DIR = os.path.join(TRAIN_DIR, "xr_UNIFESP")
MULTI_TARGET_DIR = os.path.join(SORTED_TRAIN_DIR, "xr_multi_target")

CSV_FILE = os.path.join(DATASET_DIR, "train.csv")

PYTORCH_CLASSES = {
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


# create directories if needed
def setup_directories():
    os.makedirs(MULTI_TARGET_DIR, exist_ok=True)

    # create subdirectory for each body part
    for region in PYTORCH_CLASSES.values():
        os.makedirs(os.path.join(SORTED_TRAIN_DIR, region), exist_ok=True)


# map each image id to its full path
def create_file_map():
    file_map = {}
    for root, dir_names, filenames in os.walk(UNSORTED_TRAIN_DIR):
        for f in filenames:
            if f.endswith(".dcm"):
                image_id = f.split("-")[0]
                file_map[image_id] = os.path.join(root, f)

    return file_map


# move images to named folders
def process_images(file_map):
    csv_df = pd.read_csv(CSV_FILE)
    for index, row_data in tqdm(csv_df.iterrows(), total=len(csv_df)):
        # verify file existence and get path
        image_id = row_data["SOPInstanceUID"]
        short_id = image_id[26:]  # all files have same prefix
        if image_id not in file_map:
            continue
        filepath = file_map[image_id]

        # convert and verify proper image
        png_img = dcm_to_png(filepath)
        if png_img is None:
            continue

        # save image based on number of targets
        target_str = str(row_data["Target"]).strip()
        targets = target_str.split(" ")
        if len(targets) > 1:  # multiple anatomical regions
            save_path = os.path.join(MULTI_TARGET_DIR, f"{'_'.join(targets)}_{short_id}.png")
            png_img.save(save_path)
        else:
            target = int(targets[0])
            save_dir = PYTORCH_CLASSES[target]
            save_path = os.path.join(SORTED_TRAIN_DIR, save_dir, f"{short_id}.png")
            png_img.save(save_path)


def main():
    setup_directories()
    file_map = create_file_map()

    print("IMPORTANT NOTES:")
    print("- All files will be saved in data/train/xr_UNIFESP/xr_[bodypart]")
    print("- Images with multiple targets will be placed in .../xr_UNIFESP/xr_multi_target")
    print("- There is no file or labeling for the test folder so it will be discarded")
    print("- Manual review and transfer is required before training\n")

    process_images(file_map)


if __name__ == "__main__":
    main()
