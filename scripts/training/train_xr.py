from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

CROP_SIZE = 224  # preprocessing scripts made images 256x256
BATCH_SIZE = 32


def setup_data(crop_size, train_dir, val_dir, batch_size):
    data_transforms = {
        "train": transforms.Compose([transforms.RandomCrop(crop_size), transforms.ToTensor()]),
        "val": transforms.Compose([transforms.CenterCrop(crop_size), transforms.ToTensor()]),
    }

    image_datasets = {
        "train": datasets.ImageFolder(train_dir, data_transforms["train"]),
        "val": datasets.ImageFolder(val_dir, data_transforms["val"]),
    }

    dataloaders = {
        "train": DataLoader(image_datasets["train"], batch_size=batch_size, shuffle=True),
        "val": DataLoader(image_datasets["val"], batch_size=batch_size, shuffle=False),
    }

    return image_datasets, dataloaders


def setup_model(num_classes, device):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)  # using resnet18
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    model = model.to(device)


def main():
    setup_data(CROP_SIZE, TRAIN_DIR, VAL_DIR, BATCH_SIZE)


if __name__ == "__main__":
    main()
