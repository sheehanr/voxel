import os
import sys


def print_directory_stats(path):
    if not os.path.exists(path):
        print(f"Error: Directory '{path}' not found.")
        return

    total_files = 0
    subdir_counts = {}

    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            count = len(
                [
                    f
                    for f in os.listdir(item_path)
                    if os.path.isfile(os.path.join(item_path, f))
                ]
            )
            subdir_counts[item] = count
            total_files += count
        elif os.path.isfile(item_path):
            total_files += 1

    print(f"--- Statistics for: {os.path.basename(path)} ---")
    print(f"Total Files: {total_files}")
    print("Breakdown:")
    for folder, count in subdir_counts.items():
        print(f"  - {folder}: {count}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_data.py <path_to_directory>")
    else:
        target_dir = sys.argv[1]
        print_directory_stats(target_dir)
