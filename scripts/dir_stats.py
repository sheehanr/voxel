import sys
from pathlib import Path


def get_dir_stats(path):
    if not path.exists():
        print(f"ERROR [print_dir_stats]: Directory '{path}' not found.")
        return -1, -1, {}

    file_count = 0
    total_bytes = 0
    stats = {}

    for item in sorted(path.iterdir()):
        if item.is_dir():
            count = 0
            size = 0

            for f in item.rglob("*"):
                if f.is_file() and not f.is_symlink():
                    count += 1
                    size += f.stat().st_size

            stats[item.name] = (count, size)
            file_count += count
            total_bytes += size

        elif item.is_file() and not item.is_symlink():
            file_count += 1
            total_bytes += item.stat().st_size

    return file_count, total_bytes, stats


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024

    return f"{size_bytes:.2f} TB"


def print_dir_stats(path):
    path = Path(path)

    file_count, total_bytes, stats = get_dir_stats(path)
    if file_count < 0:
        return

    name = path.name if path.name else path.resolve().name

    print(f"\n--- Statistics for: {name} ---")
    print(f"\nTotal Files: {file_count}")
    print(f"Total Size:  {format_size(total_bytes)}")

    show_breakdown = input("\nShow breakdown? (y/n): ")

    if show_breakdown.lower() == "y":
        print("\nBreakdown:")

        for folder, (count, size) in stats.items():
            print(f"  - {folder}: {count} files ({format_size(size)})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dir_stats.py <path_to_directory>")
        return

    path = sys.argv[1]
    print_dir_stats(path)


if __name__ == "__main__":
    main()
