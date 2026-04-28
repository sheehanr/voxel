import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms



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


def main():
    setup_data(CROP_SIZE, TRAIN_DIR, VAL_DIR, BATCH_SIZE)


if __name__ == "__main__":
    main()
