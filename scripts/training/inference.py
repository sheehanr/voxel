import sys
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

SCRIPT_DIR = Path(__file__).resolve().parent

DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

MODELS_DIR = (SCRIPT_DIR / "../../models").resolve()
WTS_PATH = MODELS_DIR / "best_acc_model.pth"

OG_SIZE = 256
CROP_SIZE = 224

DEVICE = torch.device("cuda")

CLASSES = [
    "xr_ankle",
    "xr_chest",
    "xr_elbow",
    "xr_finger",
    "xr_foot",
    "xr_forearm",
    "xr_hand",
    "xr_hip",
    "xr_humerus",
    "xr_knee",
    "xr_other",
    "xr_shoulder",
    "xr_wrist",
]


def main():
    pass


if __name__ == "__main__":
    main()
