"""
    author: Parisa Daj
    date: May 10, 2022
    Crop image into patches
"""
import glob
import os

from utils import crop2patches


def main():
    """
    todo: fairsim third dimension: z0 5 phases 1 angle -> [5 5 5 5 5][5 5 5 5 5][5 5 5 5 5]
    """
    data_path = 'D:\\Data\\datasets_ryan\\test\\'
    x, y, z = [128, 128, 5]
    cropped_path = 'D:\\Data\\datasets_ryan\\cropped\\'

    phases = 5
    angles = 3
    if not os.path.exists(cropped_path):
        os.mkdir(cropped_path)
    ns_channels = [phases * angles, 1]

    folders = glob.glob(data_path + '*\\')
    out_folders = dict()
    imgs_paths = dict()
    for folder in folders:
        folder_name = folder.split('\\')[-2]
        out_folders[folder_name] = os.path.join(cropped_path, folder_name)

        if not os.path.exists(out_folders[folder_name]):
            os.mkdir(out_folders[folder_name])

        imgs_paths[folder_name] = glob.glob(folder + '*.tif')

        scale = 2 if 'gt' in folder_name else 1
        n_channels = 1 if 'gt' in folder_name else phases * angles

        for img_path in imgs_paths[folder_name]:
            patch_sizes = [z, x * scale, y * scale]

            crop2patches(img_path, out_folders[folder_name], patch_sizes, n_channels)

if __name__ == '__main__':
    main()
