from glob import glob

import numpy as np
import skimage as sk
import skimage.io as skio
import os


def shift(image, displacement):
    '''
    Shifts image by a given displacement
    :param image:
    :param displacement: [x,y]
    :return: shifted image
    '''
    return np.roll(np.roll(image, displacement[0], axis=0), displacement[1], axis=1)

def calc_ssd(img1, img2):
    '''
    Computes the sum of squared distance metric for image 1 and image 2
    :return: ssd metric
    '''
    return np.sum(np.sum(np.square(img1 - img2)))


def align_ssd(img1, img2, search_range=20):
    '''
    Aligns two images with SSD
    :param img1: Image 1
    :param img2: Image 2
    :param search_range: Range of displacements to search over.
    :return: Displacements [i, j]
    '''
    best_displacement = [0, 0]
    best_ssd = calc_ssd(img1, img2)
    for i in range(-1 * search_range, search_range):
        for j in range(-1 * search_range, search_range):
            img1_shifted = shift(img1, [i, j])
            ssd = calc_ssd(img1_shifted, img2)
            if ssd < best_ssd:
                best_ssd = ssd
                best_displacement = [i, j]
    return best_displacement


def align_pyramid(img1,
                  img2,
                  recursion_count=0,
                  ssd_min_res=500,
                  rescale_factor=0.5,
                  corrected_crop_size=100):
    '''
    Uses pyramid alignment to return the displacement for two images
    :param img1:
    :param img2:
    :param recursion_count: recursion counter to be incremented at every call
    :param ssd_min_res: Minimum resolution requirement to invoke align_ssd
    :param rescale_factor: Rescaling factor for the pyramid
    :param corrected_crop_size: Crop size to use for computing displacement error
    :return: displacement [x,y]
    '''
    if ((img1.shape[0] <= ssd_min_res) and (img2.shape[0] <= ssd_min_res)) or (recursion_count == 10):
        # Recursion end condition, image is small enough to run ssd or recursion has hit limit
        return align_ssd(img1, img2)
    else:
        # Recursively call displacement
        displacement = align_pyramid(sk.transform.rescale(img1, rescale_factor),
                                     sk.transform.rescale(img2, rescale_factor),
                                     recursion_count = recursion_count + 1)
        # Rescale displacement
        displacement = [int(displacement[0]/rescale_factor), int(displacement[1]/rescale_factor)]

        # Compute the displacement error for the higher resolution image but only for a cropped region
        crop_x = (img1.shape[0] // 2) - corrected_crop_size
        crop_y = (img1.shape[1] // 2) - corrected_crop_size

        corrected_img1 = shift(img1, displacement)
        corrected_cropped_img1 = corrected_img1[crop_x: -1 * crop_x, crop_y: -1 * crop_y]
        cropped_img2 = img2[crop_x: -1*crop_x, crop_y: -1*crop_y]
        displacement_error = align_ssd(corrected_cropped_img1, cropped_img2)

        # Apply error correction to displacement and return
        return [displacement[0] + displacement_error[0], displacement[1] + displacement_error[1]]


def colorize(filepath,
             method='pyramid',
             center_crop_margin=0,
             edge_filter_fn=sk.filters.sobel,
             out_base_dir=None):
    '''
    Wrapper function to colorize images. Writes results to disk.
    :param filepath: Path to image
    :param method: either pyramid or ssd
    :param center_crop_margin: Center cropping to remove black bands
    :param edge_filter_fn: one of sk.filters functions to compute edges.
    :param out_base_dir: Output dir
    '''
    # read in the image
    im = skio.imread(filepath)

    # convert to double (might want to do this later on to save memory)
    im = sk.img_as_float(im)

    # compute the height of each part (just 1/3 of total)
    height = int(np.floor(im.shape[0] / 3.0))

    # separate color channels
    b = im[:height]
    g = im[height: 2 * height]
    r = im[2 * height: 3 * height]

    # Crop bands if required
    if center_crop_margin == 0:
        cropped_b = b
        cropped_g = g
        cropped_r = r
    else:
        cropped_b = b[center_crop_margin:-1 * center_crop_margin, center_crop_margin:-1 * center_crop_margin]
        cropped_g = g[center_crop_margin:-1 * center_crop_margin, center_crop_margin:-1 * center_crop_margin]
        cropped_r = r[center_crop_margin:-1 * center_crop_margin, center_crop_margin:-1 * center_crop_margin]

    # Edge detection for better matching
    edge_b = edge_filter_fn(cropped_b)
    edge_g = edge_filter_fn(cropped_g)
    edge_r = edge_filter_fn(cropped_r)

    # Run the alignment method to get displacement
    if method == 'pyramid':
        ag_displacement = align_pyramid(edge_g, edge_b)
        ar_displacement = align_pyramid(edge_r, edge_b)
    elif method == 'ssd':
        ag_displacement = align_ssd(edge_g, edge_b)
        ar_displacement = align_ssd(edge_r, edge_b)

    print("{}: [{},{}]".format(filepath, ag_displacement[0], ag_displacement[1]))

    # Shift
    ag = shift(g, ag_displacement)
    ar = shift(r, ar_displacement)

    # Create color image
    im_out = np.dstack([ar, ag, b])

    # save the image
    if out_base_dir:
        name = os.path.splitext(os.path.basename(filepath))[0]
        out_filename = 'recolorized_' + name + '.jpeg'
        out_path = os.path.join(out_base_dir, out_filename)
        skio.imsave(out_path, im_out)


if __name__ == '__main__':
    out_base_dir = 'output_imgs'
    in_base_dir = 'example_imgs'
    small_images = glob(os.path.join(in_base_dir, '*.jpg'))
    large_images = glob(os.path.join(in_base_dir, '*.tif'))
    print("Found JPGs: {}".format(small_images))
    print("Found tiffs: {}".format(large_images))

    for filepath in small_images:
        colorize(filepath,
                 method='ssd',
                 center_crop_margin=10,
                 out_base_dir=out_base_dir)

    for filename in large_images:
        colorize(filename,
                 method='pyramid',
                 # edge_filter_fn=lambda x: x,
                 out_base_dir=out_base_dir)
