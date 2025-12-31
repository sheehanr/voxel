import os
import zipfile

from kaggle.api.kaggle_api_extended import KaggleApi
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../data"))
DOWNLOADS_DIR = os.path.join(DATA_DIR, "downloads")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")


# create directories if needed
def init_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(VAL_DIR, exist_ok=True)


# create directories and download datasets in them
def download_datasets():
    api = KaggleApi()
    api.authenticate()

    # dictionary key corresponds to name of directory
    datasets = {
        "TUSEB_ct_brain": "ozguraslank/brain-stroke-ct-dataset",
        "TCIA_ct_chest": "kmader/siim-medical-images",
        "MH_ct_chest": "mohamedhanyyy/chest-ctscan-images",
        "IQOTHNCCD_ct_chest": "adityamahimkar/iqothnccd-lung-cancer-dataset",
        "MN_mr_brain": "masoudnickparvar/brain-tumor-mri-dataset",
        "AIMI_mr_knee": "cjinny/mrnet-v1",
        "NIH_xr_chest": "nih-chest-xrays/data",
        "AIMI_xr_upper": "cjinny/mura-v11",
        "UNIFESP_xr_fullbody": "felipekitamura/unifesp-xray-bodypart-classification",
        "MD_xr_knee": "orvile/digital-knee-x-ray-images",
        "MG_xr_knee": "mohamedgobara/multi-class-knee-osteoporosis-x-ray-dataset",
        "OT_xr_heel": "osamahtaher/heel-dataset",
    }

    competitions = {"RSNA_mr_spine": "rsna-2024-lumbar-spine-degenerative-classification"}

    for dir, slug in tqdm(datasets.items(), desc="\nDownloading Datasets"):
        dst = os.path.join(DOWNLOADS_DIR, dir)

        if os.path.exists(dst):
            print(f"\n{dir} already exists, skipping...")
            continue

        try:
            api.dataset_download_files(slug, path=dst, unzip=True)

        except Exception:
            print(f"\nUnable to download {dir}")
            print("\nTry downloading the dataset using the following command in your terminal:")
            print(f"kaggle datasets download {slug}")
            print("\nOr, download the dataset from the dataset webpage:")
            print(f"https://www.kaggle.com/datasets/{slug}")

    for dir, slug in tqdm(competitions.items(), desc="\nDownloading Datasets"):
        dst = os.path.join(DOWNLOADS_DIR, dir)

        if os.path.exists(dst):
            print(f"\n{dir} already exists, skipping...")
            continue

        try:
            api.competition_download_files(slug, path=dst)

            # competitions do not support unzip=True
            zip_name = slug + ".zip"
            zip_path = os.path.join(dst, zip_name)

            if os.path.exists(zip_path):
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(dst)
                os.remove(zip_path)

        except Exception:
            print(f"\nUnable to download {dir}")
            print("\nTry downloading the dataset using the following command in your terminal:")
            print(f"kaggle competitions download -c {slug}")
            print("\nOr, download the dataset from the competition webpage:")
            print(f"https://www.kaggle.com/competitions/{slug}/data")


def main():
    print("WARNING: This script will download ~90GB of data to your computer.")
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != "y":
        return

    init_dirs()
    download_datasets()


if __name__ == "__main__":
    main()
