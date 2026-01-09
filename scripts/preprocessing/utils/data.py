import random


# randomly separate files into train and val
def split_data(file_list, split_ratio=0.9):
    random.shuffle(file_list)
    n_train = int(len(file_list) * split_ratio)

    train_files = file_list[:n_train]
    val_files = file_list[n_train:]

    return train_files, val_files


# randomly select files from list
def sample_files(file_list, n=5500):
    return random.sample(file_list, n)
