"""
    Necessary functions for 3D deep learning process
    including crop to 3D patches

    Author: Parisa Daj
    Date: 12 May, 2022
"""
import glob
import os
import numpy as np
import tifffile as tiff


def crop2patches(in_path: str, out_path: str, patch_sizes: list, n_channels: int = 15):
    """
        Crop given image to 3D patches of given size

    :param in_path: path to read the image from (tiff format)
    :param out_path: path to save the cropped images to (tiff formet: same name + x, y, z ids)
    :param patch_sizes: a list of each patch size (integers) in order of z, x, y
    :param n_channels: phases * angles
    :return:

    todo: separate last patch to have the most info from the original image
    todo: number of patches can be independent of patch sizes
    """
    img = tiff.imread(in_path)
    img_name = in_path.split('\\')[-1].split('.tif')[0]
    if 'ER' in img_name:
        img_name = img_name.replace('ER', 'E')
    img_name = img_name.replace('E_Sample_', '')

    shape = list(np.shape(img))
    shape[0] = shape[0] // n_channels

    # make them compatible with 3d analysis
    if len(shape) == 2:
        shape.insert(0, 1)
        img = np.reshape(img, (shape[0], shape[1], shape[2]))

    n_patches = [0] * len(shape)
    overlaps = [0] * len(shape)
    for i, patch in enumerate(patch_sizes):
        # number of patches in each axis
        n_patches[i] = int(np.ceil(shape[i] / patch))
        # overlapping distance in each axis
        if n_patches[i] > 1:
            overlaps[i] = int((shape[i] - patch) // (n_patches[i] - 1))
        else:
            overlaps[i] = 0
    # print(in_path)
    # print(n_patches)
    # print(overlaps)

    for z in range(n_patches[0]):
        for x in range(n_patches[1]):
            for y in range(n_patches[2]):
                final_path = os.path.join(out_path,
                                          img_name + '_' +
                                          str(x) + str(y) + str(z) + '.tiff')
                if not os.path.exists(out_path):
                    os.mkdir(out_path)

                new_img = img[(overlaps[0] * z) * n_channels:
                              (overlaps[0] * z + patch_sizes[0]) * n_channels,
                              overlaps[1] * x: overlaps[1] * x + patch_sizes[1],
                              overlaps[2] * y: overlaps[2] * y + patch_sizes[2]]
                with tiff.TiffWriter(final_path) as t:
                    t.write(new_img)