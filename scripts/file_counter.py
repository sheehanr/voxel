import os
import sys


def get_size(path):
    size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp):
                size += os.path.getsize(fp)

    return size


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024

    return f"{size_bytes:.2f} TB"


def get_dir_stats(path):
    if not os.path.exists(path):
        print(f"ERROR [print_dir_stats]: Directory '{path}' not found.")
        return -1, -1, {}

    file_count = 0
    total_bytes = 0
    stats = {}

    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            count = 0
            for root, dirs, files in os.walk(item_path):
                count += len(files)

            size = get_size(item_path)

            stats[item] = (count, size)
            file_count += count
            total_bytes += size

        elif os.path.isfile(item_path):
            file_count += 1
            total_bytes += os.path.getsize(item_path)

    return file_count, total_bytes, stats


def print_dir_stats(path, file_count, total_bytes, stats):
    print(f"\n--- Statistics for: {os.path.basename(path)} ---")
    print(f"\nTotal Files: {file_count}")
    print(f"Total Size:  {format_size(total_bytes)}")

    show_breakdown = input("\nShow breakdown? (y/n): ")

    if show_breakdown.lower() == "y":
        print("\nBreakdown:")

        for folder, (count, size) in stats.items():
            print(f"  - {folder}: {count} files ({format_size(size)})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 file_counter.py <path_to_directory>")
        return

    path = sys.argv[1]
    file_count, total_bytes, stats = get_dir_stats(path)
    if file_count > -1:
        print_dir_stats(path, file_count, total_bytes, stats)


if __name__ == "__main__":
    main()
