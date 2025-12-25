import os

UNSORTED_PATH = "../../data/unsorted/unifesp/train"
SORTED_PATH = "../../data/unsorted/unifesp/sorted_train"

CSV_PATH = "../../data/unsorted/unifesp/train.csv"
TARGET_DIMENSIONS = (256, 256)

ANATOMICAL_REGIONS = {
    0: "Abdomen",
    1: "Ankle",
    2: "Cervical Spine",
    3: "Chest",
    4: "Clavicles",
    5: "Elbow",
    6: "Feet",
    7: "Finger",
    8: "Forearm",
    9: "Hand",
    10: "Hip",
    11: "Knee",
    12: "Lower Leg",
    13: "Lumbar Spine",
    14: "Others",
    15: "Pelvis",
    16: "Shoulder",
    17: "Sinus",
    18: "Skull",
    19: "Thigh",
    20: "Thoracic Spine",
    21: "Wrist",
}

# create needed directories if they do not already exist
os.makedirs(SORTED_PATH, exist_ok=True)
for region in ANATOMICAL_REGIONS.values():  # creates a subdirectory in SORTED_PATH for each anatomical region
    os.makedirs(os.path.join(SORTED_PATH, region), exist_ok=True)