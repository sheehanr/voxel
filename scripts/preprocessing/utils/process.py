from pathlib import Path

from PIL import Image
from tqdm import tqdm

from utils import load_dcm, split_data, standardize_pil

IMG_SIZE = (256, 256)


# handle file according to extension; return img and check_inversion
def handle_file(filepath, check_inversion):
    ext = filepath.suffix.lower()

    if ext == ".dcm":
        return load_dcm(filepath), False

    elif ext in [".jpg", ".jpeg", ".png"]:
        return Image.open(filepath), check_inversion

    return None, True


# get destination path
def get_dst_path(filename, dst_dir, prefix, custom_name):
    if custom_name:
        filename = custom_name

    if prefix:
        filename = f"{prefix}{filename}"

    return dst_dir / f"{filename}.png"


# load, process, and save image
def process_image(filepath, dst_dir, prefix=None, custom_name=None, check_inversion=True, img_size=IMG_SIZE):
    filepath = Path(filepath)
    dst_dir = Path(dst_dir)

    if not filepath.exists():
        print(f"ERROR [process_image]: {filepath} not found")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)

    img, check_inversion = handle_file(filepath, check_inversion)
    if img is None:
        return

    # standardize and save as png
    img = standardize_pil(img, img_size, check_inversion)

    filename = filepath.stem
    dst_path = get_dst_path(filename, dst_dir, prefix, custom_name)
    img.save(dst_path)


# loop through each file in the allowlist for a class
def process_class_files(class_name, file_list, file_map, dst_map, prefix_func, custom_name_func, pbar):
    for f in file_list:
        if f in file_map:
            filepath = file_map[f]
            prefix, custom_name = None, None

            if prefix_func:
                prefix = prefix_func(f)
            if custom_name_func:
                custom_name = custom_name_func(filepath)

            process_image(filepath, dst_map[class_name], prefix, custom_name)
            pbar.update(1)


# loop to process files for datasets with multiple classes and a custom allowlist
def process_classes(class_lists_map, file_map, train_dst_map, val_dst_map, prefix_func=None, custom_name_func=None):
    total_files = sum(len(files) for files in class_lists_map.values())
    with tqdm(total=total_files, desc="Processing files") as pbar:
        for class_name, file_list in class_lists_map.items():
            train_files, val_files = split_data(file_list)

            process_class_files(class_name, train_files, file_map, train_dst_map, prefix_func, custom_name_func, pbar)
            process_class_files(class_name, val_files, file_map, val_dst_map, prefix_func, custom_name_func, pbar)
