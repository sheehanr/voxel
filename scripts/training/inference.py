import random
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


def load_model(wts_path, device, classes):
    model = models.resnet18(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(classes))

    model.load_state_dict(torch.load(wts_path, map_loaction=device, weights_only=True))
    model = model.to(device)
    model.eval()
    return model


def predict(img_path, model, device, resize, crop_size, classes):
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"ERROR: Unable to load image ({e})")
        return

    transform = transforms.Compose([transforms.Resize(resize), transforms.CenterCrop(crop_size), transforms.ToTensor()])

    input_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    top3_prob, top3_idx = torch.topk(probabilities, 3)

    print("\n" + "-" * 30)
    print(f"File: {'/'.join(img_path.parts[-3:])}")
    print("-" * 30)

    for i in range(3):
        class_name = classes[top3_idx[i].item()]
        confidence = top3_prob[i].item() * 100
        print(f"{i + 1}: {class_name} ({confidence:.2f}%)")
    print("-" * 30)


def pick_random_img(data_dir):
    exts = ["*.jpg", "*.jpeg", "*.png"]
    img_paths = []
    for ext in exts:
        img_paths.extend(list(data_dir.rglob(ext)))

    if not img_paths:
        return None

    return random.choice(img_paths)


def main():
    pass


if __name__ == "__main__":
    main()
