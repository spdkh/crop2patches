"""
    author: Parisa Daj
    date: May 10, 2022
    Crop image into patches
"""
import glob
import os

from utils import crop2patches


DATA_PATH = 'D:\\Data\\FixedCell\\PFA_eGFP\\data\\'
N_X, N_Y, N_Z = [128, 128, 1]
CROPPED_PATH = 'D:\\Data\\FixedCell\\PFA_eGFP\\cropped2d\\'

N_PHASES = 5
N_ANGLES = 3


def main():
    """
        Go through raw data and ground truth folders in the given folder
        crop all tiff images within these two folder to the given x, y, z
        Please specify DATA_PATH, x, y, z, CROPPED_PATH, N_PHASES, N_ANGLES
        in the DATA_PATH folder there have to be two subfolders:
        1. the raw data folder with any given name (the name should not include "gt")
        2. the ground truth folder with any given name followed by "gt"
    """
    if not os.path.exists(CROPPED_PATH):
        os.mkdir(CROPPED_PATH)

    folders = glob.glob(DATA_PATH + '*\\')
    out_folders = dict()
    imgs_paths = dict()
    for folder in folders:
        print(folder)
        folder_name = folder.split('\\')[-2]
        out_folders[folder_name] = os.path.join(CROPPED_PATH, folder_name)

        if not os.path.exists(out_folders[folder_name]):
            os.mkdir(out_folders[folder_name])

        imgs_paths[folder_name] = glob.glob(folder + '*.tif')

        scale = 2 if 'gt' in folder_name else 1
        n_phases = 1 if 'gt' in folder_name else N_PHASES
        n_angles = 1 if 'gt' in folder_name else N_ANGLES

        for img_path in imgs_paths[folder_name]:
            patch_sizes = [N_Z, N_X * scale, N_Y * scale]

            crop2patches(img_path, out_folders[folder_name], patch_sizes, n_phases, n_angles)


if __name__ == '__main__':
    main()
