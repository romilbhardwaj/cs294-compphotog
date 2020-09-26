import numpy as np
import skimage as sk
import skimage.io as skio
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import convolve2d
from scipy.signal.windows import gaussian
from skimage.color import rgb2gray
from scipy.ndimage.interpolation import rotate
from skimage.transform import rescale, resize
from scipy.ndimage import gaussian_filter
import cv2
import os
from align_image_code import align_images

def get_gaussian(size, sigma):
    kernel = cv2.getGaussianKernel(size, sigma)
    return np.outer(kernel, np.transpose(kernel))

def blur(image, gaussian_kernel):
    channelwise_blur = []
    for channel in range(image.shape[2]):
        s = convolve2d(image[:,:,channel], gaussian_kernel, mode="same").reshape([image.shape[0], image.shape[1], 1])
        channelwise_blur.append(s)
    blurred_img = np.dstack(channelwise_blur)
    return blurred_img

def save_fft(out_path, im):
    plt.figure(figsize=(10, 10))
    plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(im)))))
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')

# Creates a hybrid image
def hybrid_image(im1, im2, gaussian_kernel, save_intermediates=False):
    im1, im2 = align_images(im1, im2)
    # Normalize images
    im1 = im1 / np.max(im1)
    im2 = im2 / np.max(im2)
    # Low pass filter first image
    lpf_im1 = blur(im1, gaussian_kernel)
    lpf_im2 = blur(im2, gaussian_kernel)
    # Get high frequencies for image 2
    hpf_im2 = im2 - lpf_im2
    # Average images
    hybrid = (lpf_im1 + hpf_im2)/2

    if save_intermediates:
        os.makedirs('outputs/hybrid/fft/', exist_ok=True)
        save_fft('outputs/hybrid/fft/im1.jpg', rgb2gray(im1))
        save_fft('outputs/hybrid/fft/im2.jpg', rgb2gray(im2))
        save_fft('outputs/hybrid/fft/lpf_im1.jpg', rgb2gray(lpf_im1))
        save_fft('outputs/hybrid/fft/hpf_im2.jpg', rgb2gray(hpf_im2))
        save_fft('outputs/hybrid/fft/hybrid.jpg', rgb2gray(hybrid))

    return hybrid

gaussian_kernel = get_gaussian(20, 10)
im1 = skio.imread('imgs/hybrids/DerekPicture.jpg')
im2 = skio.imread('imgs/hybrids/nutmeg.jpg')
h = hybrid_image(im1, im2, gaussian_kernel, save_intermediates=True)
skio.imsave("outputs/hybrid/dereknutmeg.jpg", h)


gaussian_kernel = get_gaussian(10, 5)
im2 = skio.imread('imgs/hybrids/palpatine.png')
im1 = skio.imread('imgs/hybrids/obiwan.jpg')
h = hybrid_image(im1, im2, gaussian_kernel, save_intermediates=False)
skio.imsave("outputs/hybrid/palpatinekenobi.jpg", h)

gaussian_kernel = get_gaussian(10, 5)
im1 = skio.imread('imgs/hybrids/vader.jpg')
im2 = skio.imread('imgs/hybrids/luke.jpg')
h = hybrid_image(im1, im2, gaussian_kernel, save_intermediates=True)
skio.imsave("outputs/hybrid/lukevader.jpg", h)