import zipfile
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = (SCRIPT_DIR / "../data").resolve()

DOWNLOADS_DIR = DATA_DIR / "downloads"
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "val"

DATASETS = {  # dictionary key corresponds to name of directory
    "ct_brain_TUSEB": "ozguraslank/brain-stroke-ct-dataset",
    "ct_chest_TCIA": "kmader/siim-medical-images",
    "ct_chest_MH": "mohamedhanyyy/chest-ctscan-images",
    "ct_chest_IQOTHNCCD": "adityamahimkar/iqothnccd-lung-cancer-dataset",
    "mr_brain_MN": "masoudnickparvar/brain-tumor-mri-dataset",
    "mr_knee_AIMI": "cjinny/mrnet-v1",
    "xr_chest_NIH": "nih-chest-xrays/data",
    "xr_upper_AIMI": "cjinny/mura-v11",
    "xr_fullbody_UNIFESP": "felipekitamura/unifesp-xray-bodypart-classification",
    "xr_knee_MD": "orvile/digital-knee-x-ray-images",
    "xr_knee_MG": "mohamedgobara/multi-class-knee-osteoporosis-x-ray-dataset",
    "xr_foot_OT": "osamahtaher/heel-dataset",
}

COMPETITIONS = {"mr_spine_RSNA": "rsna-2024-lumbar-spine-degenerative-classification"}


# create directories if needed
def init_dirs(dir_list):
    for dir in dir_list:
        dir.mkdir(parents=True, exist_ok=True)


def download_dataset(api, downloads_dir, directory, slug):
    dst = downloads_dir / directory

    if dst.is_dir():
        print(f"\n{directory} already exists, skipping...")
        return

    try:
        api.dataset_download_files(slug, path=dst, unzip=True)

    except Exception:
        print(f"\nERROR [download_datasets]: Unable to download {directory}")
        print("\nTry downloading the dataset using the following command in your terminal:")
        print(f"kaggle datasets download {slug}")
        print("\nOr, download the dataset from the dataset webpage:")
        print(f"https://www.kaggle.com/datasets/{slug}")


def download_competition(api, downloads_dir, directory, slug):
    dst = downloads_dir / directory

    if dst.is_dir():
        print(f"\n{directory} already exists, skipping...")
        return

    try:
        api.competition_download_files(slug, path=str(dst))

        # competitions do not support unzip=True
        zip_path = dst / f"{slug}.zip"

        if zip_path.exists():
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(dst)

            zip_path.unlink()

    except Exception:
        print(f"\nERROR [download_datasets]: Unable to download {directory}")
        print("\nTry downloading the dataset using the following command in your terminal:")
        print(f"kaggle competitions download -c {slug}")
        print("\nOr, download the dataset from the competition webpage:")
        print(f"https://www.kaggle.com/competitions/{slug}/data")


# create directories and download datasets in them
def kaggle_setup(downloads_dir, datasets, competitions):
    api = KaggleApi()
    api.authenticate()

    for directory, slug in tqdm(datasets.items(), desc="\nDownloading datasets"):
        download_dataset(api, downloads_dir, directory, slug)

    for directory, slug in tqdm(competitions.items(), desc="\nDownloading competition datasets"):
        download_competition(api, downloads_dir, directory, slug)


def main():
    print("WARNING: This script will download ~90GB of data to your computer.")
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != "y":
        return

    init_dirs([DATA_DIR, DOWNLOADS_DIR, TRAIN_DIR, VAL_DIR])
    kaggle_setup(DOWNLOADS_DIR, DATASETS, COMPETITIONS)


if __name__ == "__main__":
    main()
