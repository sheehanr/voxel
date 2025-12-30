import os
import sys


def get_size(start_path):
    total_size = 0
    for root, dir_names, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(root, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024

    return f"{size_bytes:.2f} TB"


def print_directory_stats(path):
    if not os.path.exists(path):
        print(f"Error: Directory '{path}' not found.")
        return

    total_files = 0
    total_size_bytes = 0
    subdir_stats = {}

    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            count = 0
            for root, dir_names, filenames in os.walk(item_path):
                count += len(filenames)

            size = get_size(item_path)

            subdir_stats[item] = (count, size)
            total_files += count
            total_size_bytes += size

        elif os.path.isfile(item_path):
            total_files += 1
            total_size_bytes += os.path.getsize(item_path)

    print(f"--- Statistics for: {os.path.basename(path)} ---")
    print(f"Total Files: {total_files}")
    print(f"Total Size:  {format_size(total_size_bytes)}")
    print("Breakdown:")

    for folder, (count, size) in subdir_stats.items():
        print(f"  - {folder}: {count} files ({format_size(size)})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 file_counter.py <path_to_directory>")
    else:
        target_dir = sys.argv[1]
        print_directory_stats(target_dir)
