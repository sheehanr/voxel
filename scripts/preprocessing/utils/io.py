from pathlib import Path


# return list of files in text file
def read_text_file(filepath):
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"ERROR [read_text_file]: {filepath} not found")
        return []

    with open(filepath, "r") as f:
        file_list = [line.strip() for line in f.readlines()]

    return file_list


# map each unique filename to its full path
def map_files(src_dir, exts=[".png", ".jpg", ".jpeg", ".dcm"]):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [map_files]: {src_dir} not found")
        return {}

    file_map = {}

    for f in src_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in exts:
            file_map[f.name] = f

    return file_map


# return list of subdirectories of given directory
def get_subdirs(src_dir):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [get_subdirs]: {src_dir} not found")
        return []

    subdirs = []

    for d in src_dir.iterdir():
        if d.is_dir():
            subdirs.append(d.name)

    return subdirs


# return list of all filepaths from all subdirectories in a given directory
def get_filepaths(src_dir, subdirs):
    src_dir = Path(src_dir)
    if not src_dir.exists():
        print(f"ERROR [get_filepaths]: {src_dir} not found")
        return []

    filepaths = []

    for subdir in subdirs:
        subdir_path = src_dir / subdir
        for f in subdir_path.iterdir():
            if f.is_file() and not f.name.startswith("."):
                filepaths.append(f)

    return filepaths
