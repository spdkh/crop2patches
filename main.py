"""
    author: Parisa Daj
    date: May 10, 2022
    Crop image into patches
"""
import glob
import os

from utils import crop2patches


DATA_PATH = 'D:\\Data\\datasets_luhong\\train\\'
N_X, N_Y, N_Z = [64, 64, 1]
CROPPED_PATH = 'D:\\Data\\datasets_luhong\\cropped\\'

N_PHASES = 5
N_ANGLES = 3


def main():
    """
        Go through raw data and ground truth folders in the given folder
        crop all tiff images within these two folder two the given x, y, z
        Please specify DATA_PATH, x, y, z, CROPPED_PATH, N_PHASES, N_ANGLES
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
