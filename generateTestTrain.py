import os
import random
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

all_images_dir = "lesion-diagnosis"
image_file_names = []

def prepare_folders():

    if not os.path.exists("train"):
        os.makedirs("train")
    
    if not os.path.exists("test"):
        os.makedirs("test")

    images_sub_dirs = []
    for path, dirs, files in os.walk(all_images_dir):
        for sub_dir_name in dirs:
            images_sub_dirs.append(sub_dir_name)


    for images_sub_dir in images_sub_dirs:
        # for train
        train_dir = f'train/{images_sub_dir}'
        isExist = os.path.exists(train_dir)
        if not isExist:
            os.makedirs(train_dir)

        # for test
        test_dir = f'test/{images_sub_dir}'
        isExist = os.path.exists(test_dir)
        if not isExist:
            os.makedirs(test_dir)


def copy_files_for_test_and_train():
    for path, dirs, files in os.walk(all_images_dir):
        for sub_dir_name in dirs:
            all_files_list = os.popen(f'find {all_images_dir}/{sub_dir_name}/*.JPG -type f').read().splitlines()
            images_dir = f'{all_images_dir}/{sub_dir_name}'
            all_image_files_for_class_list = []
            for path, dirs, files in os.walk(images_dir):
                for file_name in files:
                    all_image_files_for_class_list.append(file_name)
            
            all_image_files_for_class = np.asarray(all_image_files_for_class_list)
            split_horizontally_idx = int(all_image_files_for_class.shape[0]* 0.8)
            training_images = all_image_files_for_class[:split_horizontally_idx] # indexing/selection of the 80%
            testing_images = all_image_files_for_class[split_horizontally_idx:] # indexing/selection of the remaining 20% 
            
            for training_image in training_images:
                src = f'{all_images_dir}/{sub_dir_name}/{training_image}'
                dst = f'train/{sub_dir_name}/{training_image}'
                shutil.copy2(src, dst)

            for testing_image in testing_images:
                src = f'{all_images_dir}/{sub_dir_name}/{testing_image}'
                dst = f'test/{sub_dir_name}/{testing_image}'
                shutil.copy2(src, dst)


def compare_folders(path1, path2):
    ignore = [".", "..", ".DS_Store"]  # ignore these pointers/ files
    for file in os.listdir(path1):
        if file in os.listdir(path2):
            if file not in ignore:
                print('Duplicate found: %s <---------' % file)

def compare_test_and_train_dir():
    for path, dirs, files in os.walk(all_images_dir):
        for sub_dir_name in dirs:
            compare_folders(f'train/{sub_dir_name}', f'test/{sub_dir_name}')


def generate_test_and_train_datasets():
    prepare_folders()
    copy_files_for_test_and_train()
    compare_test_and_train_dir()


def view_random_image(target_dir, target_class):
    # Setup target directory (we'll view images from here)
    target_folder = target_dir+target_class

    # Get a random image path
    random_image = random.sample(os.listdir(target_folder), 1)

    # Read in the image and plot it using matplotlib
    img = mpimg.imread(target_folder + "/" + random_image[0])
    plt.imshow(img)
    plt.title(target_class)
    plt.axis("off");

    print(f"Image shape: {img.shape}") # show the shape of the image

    return img