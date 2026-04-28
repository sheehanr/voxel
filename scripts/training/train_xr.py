import torch


def main():
    print(f"PyTorch version: {torch.__version__}")

    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        print(f"Successfully connected to: {device_name}")
    else:
        print("CUDA not found. PyTorch is using the CPU.")


if __name__ == "__main__":
    main()
