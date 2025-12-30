import os

import pandas as pd
from converters import dcm_to_png
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))

# note that the test folder is not included because it is unlabeled
UNSORTED_DIR = os.path.join(DATA_DIR, "unsorted/unifesp/train")
SORTED_DIR = os.path.join(DATA_DIR, "unsorted/unifesp/sorted_train")
MULTI_DIR = os.path.join(SORTED_DIR, "multi_target")
CSV_FILE = os.path.join(DATA_DIR, "unsorted/unifesp/train.csv")

TARGET_DIMENSIONS = (256, 256)

# desired dir names
ANATOMICAL_REGIONS = {
    0: "xr_abdomen_unifesp",
    1: "xr_ankle_unifesp",
    2: "xr_cervical_spine_unifesp",
    3: "xr_chest_unifesp",
    4: "xr_clavicles_unifesp",
    5: "xr_elbow_unifesp",
    6: "xr_feet_unifesp",
    7: "xr_finger_unifesp",
    8: "xr_forearm_unifesp",
    9: "xr_hand_unifesp",
    10: "xr_hip_unifesp",
    11: "xr_knee_unifesp",
    12: "xr_lower_leg_unifesp",
    13: "xr_lumbar_spine_unifesp",
    14: "xr_others_unifesp",
    15: "xr_pelvis_unifesp",
    16: "xr_shoulder_unifesp",
    17: "xr_sinus_unifesp",
    18: "xr_skull_unifesp",
    19: "xr_thigh_unifesp",
    20: "xr_thoracic_spine_unifesp",
    21: "xr_wrist_unifesp",
}


# create needed directories if needed
def setup_directories():
    os.makedirs(SORTED_DIR, exist_ok=True)
    os.makedirs(MULTI_DIR, exist_ok=True)
    for region in ANATOMICAL_REGIONS.values():  # subdir for each body part
        os.makedirs(os.path.join(SORTED_DIR, region), exist_ok=True)


# map each image id to its full path
def create_img_map():
    img_map = {}
    for root, dirs, files in os.walk(UNSORTED_DIR):
        for file in files:
            if file.endswith(".dcm"):
                img_id = file.split("-")[0]
                img_map[img_id] = os.path.join(root, file)

    return img_map


# move images to named folders
def process_files(img_map):
    csv_df = pd.read_csv(CSV_FILE)
    for index, row_data in tqdm(csv_df.iterrows(), total=len(csv_df)):
        # verify file existence and get path
        img_id = row_data["SOPInstanceUID"]
        short_id = img_id[26:]  # all files have same prefix
        if img_id not in img_map:
            continue
        filepath = img_map[img_id]

        # convert and verify proper image
        png_img = dcm_to_png(filepath, TARGET_DIMENSIONS)
        if png_img is None:
            continue

        # save image based on number of targets
        target_str = str(row_data["Target"]).strip()
        targets = target_str.split(" ")
        if len(targets) > 1:  # multiple anatomical regions
            save_path = os.path.join(MULTI_DIR, f"{'_'.join(targets)}_{short_id}.png")
            png_img.save(save_path)
        else:
            target = int(targets[0])
            save_dir = ANATOMICAL_REGIONS[target]
            save_path = os.path.join(SORTED_DIR, save_dir, f"{short_id}.png")
            png_img.save(save_path)


def main():
    setup_directories()
    img_map = create_img_map()

    process_files(img_map)


if __name__ == "__main__":
    main()
