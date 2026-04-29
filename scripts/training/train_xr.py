import copy
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../../data").resolve()
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

CROP_SIZE = 224  # preprocessing scripts made images 256x256
BATCH_SIZE = 32
NUM_EPOCHS = 10

DEVICE = torch.device("cuda")


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

    return model


def setup_loss_and_optimizer(model, image_datasets, device):
    train_targets = image_datasets["train"].targets
    class_counts = np.bincount(train_targets)

    # increased weights for classes with less images
    total_samples = len(train_targets)
    num_classes = len(class_counts)
    class_weights = total_samples / (num_classes * class_counts)

    class_weights = torch.tensor(class_weights, dtype=torch.float).to(device)

    criterion = nn.CrossEntropyLoss(weight=class_weights)

    optimizer = optim.Adam(model.parameters(), lr=0.001)

    return criterion, optimizer


def train_model(model, dataloaders, image_datasets, criterion, optimizer, device, num_epochs=10):
    print("Starting training...")

    dataset_sizes = {x: len(image_datasets[x]) for x in ["train", "val"]}

    best_acc = 0.0
    best_wts = copy.deepcopy(model.state_dict())

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch + 1}/{num_epochs}")
        print("-" * 11)

        for phase in ["train", "val"]:
            if phase == "train":
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in tqdm(dataloaders[phase], desc=f"{phase.capitalize()} Phase", leave=False):
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)

                    _, preds = torch.max(outputs, 1)

                    loss = criterion(outputs, labels)

                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} Accuracy: {epoch_acc:.4f}")

            if phase == "val" and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_wts = copy.deepcopy(model.state_dict())

                torch.save(model.state_dict(), "best_acc_model.pth")

    print(f"\nTraining complete. Best accuracy: {best_acc:.4f}")

    model.load_state_dict(best_wts)
    return model


def main():
    image_datasets, dataloaders = setup_data(CROP_SIZE, TRAIN_DIR, VAL_DIR, BATCH_SIZE)
    class_names = image_datasets["train"].classes
    num_classes = len(class_names)
    model = setup_model(num_classes, DEVICE)
    criterion, optimizer = setup_loss_and_optimizer(model, image_datasets, DEVICE)
    model = train_model(model, dataloaders, image_datasets, criterion, optimizer, DEVICE, NUM_EPOCHS)


if __name__ == "__main__":
    main()
