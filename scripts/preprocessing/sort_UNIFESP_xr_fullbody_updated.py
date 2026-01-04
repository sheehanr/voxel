import os

from shared import init_multi_dirs, load_allowlist

DATASET_NAME = "UNIFESP_xr_fullbody"
SUFFIX = "_UNIFESP"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data"))
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

DATASET_DIR = os.path.join(DATA_DIR, "downloads", DATASET_NAME)
SRC_DIR = os.path.join(DATASET_DIR, "train")

ALLOWLIST = os.path.join(SCRIPT_DIR, "lists/UNIFESP_allowlist.txt")

CLASS_MAP = {
    "xr_abdomen_UNIFESP": "xr_other",
    "xr_ankle_UNIFESP": "xr_ankle",
    "xr_cervical_spine_UNIFESP": "xr_cervical_spine",
    "xr_chest_frontal_UNIFESP": "xr_chest",
    "xr_chest_lateral_UNIFESP": "xr_chest",
    "xr_elbow_UNIFESP": "xr_elbow",
    "xr_femur_UNIFESP": "xr_other",
    "xr_foot_UNIFESP": "xr_foot",
    "xr_forearm_UNIFESP": "xr_forearm",
    "xr_hand_UNIFESP": "xr_hand",
    "xr_hip_UNIFESP": "xr_hip",
    "xr_knee_UNIFESP": "xr_knee",
    "xr_lumbar_spine_UNIFESP": "xr_other",
    "xr_pelvis_UNIFESP": "xr_other",
    "xr_shoulder_UNIFESP": "xr_shoulder",
    "xr_skull_UNIFESP": "xr_other",
    "xr_tibia_UNIFESP": "xr_other",
    "xr_wrist_UNIFESP": "xr_wrist",
}


def main():
    train_dst_map, val_dst_map = init_multi_dirs(CLASS_MAP, TRAIN_DIR, VAL_DIR, "xr", SUFFIX)
    allowed_set = load_allowlist(ALLOWLIST)
    if allowed_set is None:
        return


if __name__ == "__main__":
    main()
