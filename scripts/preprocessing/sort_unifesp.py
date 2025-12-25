import os

UNSORTED_PATH = "../../data/unsorted/unifesp/train"
SORTED_PATH = "../../data/unsorted/unifesp/sorted_train"
CSV_PATH = "../../data/unsorted/unifesp/train.csv"
TARGET_DIMENSIONS = (256, 256)

# desired directory names
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

# creates needed dirs if not created
def create_directories():
    os.makedirs(SORTED_PATH, exist_ok=True)
    for region in ANATOMICAL_REGIONS.values():  # subdir for each body part
        os.makedirs(os.path.join(SORTED_PATH, region), exist_ok=True)

# maps each image id from train.csv to full path
def create_image_map():
    image_map = {}
    for root, dirs, files in os.walk(UNSORTED_PATH):
        for file in files:
            if file.endswith(".dcm"):
                image_id = file.split("-")[0]
                image_map[image_id] = os.path.join(root, file)

    return image_map


def main():
    create_directories()


if __name__ == "__main__":
    main()
