"""
    Necessary functions for 3D deep learning process
    including crop to 3D patches

    Author: Parisa Daj
    Date: 12 May, 2022
"""
import os
import numpy as np
import tifffile as tiff


def reorder_1(img, phases=5, angles=3):
    """
        Change the z data order from angles, z, phases
        to z, angles, phases
    :param img:
    :param phases:
    :param angles:
    :return:
    """
    [n_zs, n_x, n_y] = np.shape(img)
    n_z = n_zs // (angles * phases)
    five_d_img = np.reshape(img, (angles, n_z, phases, n_x, n_y))
    # swap angles with z
    new_img = five_d_img.swapaxes(1, 0)
    return np.reshape(new_img, (n_zs, n_x, n_y))


def reorder_2(img, phases=5, angles=3):
    """
        Change the z data order from z, angles, phases
        to angles, z, phases
    :param img:
    :param phases:
    :param angles:
    :return:
    """
    [n_zs, n_x, n_y] = np.shape(img)
    n_z = n_zs // (angles * phases)
    five_d_img = np.reshape(img, (n_z, angles, phases, n_x, n_y))
    # swap angles with z
    new_img = five_d_img.swapaxes(1, 0)
    return np.reshape(new_img, (n_zs, n_x, n_y))


def crop2patches(in_path: str, out_path: str, patch_sizes: list,
                 n_phases: int = 5, n_angles: int = 3):
    """
        Crop given image to 3D patches of given size

    :param in_path: path to read the image from (tiff format)
    :param out_path: path to save the cropped images to (tiff formet: same name + x, y, z ids)
    :param patch_sizes: a list of each patch size (integers) in order of z, x, y
    :param n_phases
    :param n_angles
    :return:

    todo: separate last patch to have the most info from the original image
    todo: number of patches can be independent of patch sizes!?!
    """
    n_channels = n_phases * n_angles
    img = tiff.imread(in_path)

    #  Change the z data order of the input data
    if n_channels != 1:
        img = reorder_1(img)

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

    for k in range(n_patches[0]):
        for i in range(n_patches[1]):
            for j in range(n_patches[2]):
                final_path = os.path.join(out_path,
                                          img_name + '_' +
                                          str(i) + str(j) + str(k) + '.tiff')

                if not os.path.exists(out_path):
                    os.mkdir(out_path)

                new_img = img[(overlaps[0] * k) * n_channels:
                              (overlaps[0] * k + patch_sizes[0]) * n_channels,
                          overlaps[1] * i: overlaps[1] * i + patch_sizes[1],
                          overlaps[2] * j: overlaps[2] * j + patch_sizes[2]]

                # return the order of 3rd dimension to the original style
                if n_channels != 1:
                    new_img = reorder_2(new_img)

                with tiff.TiffWriter(final_path) as tif:
                    tif.write(new_img)
