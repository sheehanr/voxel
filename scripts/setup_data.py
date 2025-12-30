import os

from kaggle.api.kaggle_api_extended import KaggleApi

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../data"))
DOWNLOADS_DIR = os.path.join(DATA_DIR, "downloads")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")


# create directories if needed
def setup_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(VAL_DIR, exist_ok=True)


def download_datasets():
    api = KaggleApi()
    api.authenticate()

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


def main():
    pass


if __name__ == "__main__":
    main()
