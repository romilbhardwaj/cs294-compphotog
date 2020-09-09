CS294-26 - Project 1 - Colorizing the Prokudin-Gorskii photo collection
=======================================================================

Overview
--------

The goal of this assignment is to take the digitized Prokudin-Gorskii glass plate images and, using image processing techniques, automatically produce a color image with as few visual artifacts as possible. In order to do this, we extract the three color channel images, place them on top of each other, and align them so that they form a single RGB color image.

Approach
--------

1\. **Channel extraction:** First step is to extract the three images into blue, green and red channels. This is done by splitting the input image plate into three equally sized images.

2\. **Crop bands, if required:** Using a constant crop margin, crop the channels to remove the black bands at the edges

3\. **Compute edges for matching:** While it is possible to directly align RGB images, I added edge detection to make the matching faster and more accurate. I use the sobel edge detector from sklearn.

4\. **Run alignment:** Images can be aligned by exhaustively searching for an optimal x,y displacement which minimizes the [Sum of Squared Distance](https://en.wikipedia.org/wiki/Mean_squared_error) between the edges of two images. I used a search space of +-20px. However, this can get slow for larger high resolution images. To speed up SSD, we use an image pyramid which recursively computes SSD on a sub-sampled image. It reduces the search space by running SSD on a smaller image, then using the displacement estimates on a cropped region in the higher resolution image to correct the estimates and recursively repeats.

Notes
-----

Cropping the black bands had mixed results - it was helpful for the smaller jpgs when directly running SSD, but it made results worse and some images would not align well.

Bells and Whistles
------------------

Instead of running SSD on RGB channels, I computed the edges of images and used that as a feature for alignment. This has two benefits - it reduces the runtime complexity and the output images were much sharper. For instance, compare the Melons and Emir results:

### Emir with Edge Detection

![](output_imgs/recolorized_emir.jpeg)

### Emir without Edge Detection

![](output_imgs/recolorized_emir_noedge.jpeg)

### Melons with Edge Detection (Zoom In)

![](output_imgs/recolorized_melons_noedge.jpeg)

### Melons without Edge Detection (Zoom In)

![](output_imgs/recolorized_melons_noedge.jpeg)

Example Images and displacements
--------------------------------

### cathedral: Red \[12,3\], Green \[5,2\]

![](output_imgs/recolorized_cathedral.jpeg)

### monastery: Red \[3,0\], Green \[-3,0\]

![](output_imgs/recolorized_monastery.jpeg)

### harvesters: Red \[123,18\], Green \[59,19\]

![](output_imgs/recolorized_harvesters.jpeg)

### train: Red \[85,32\], Green \[42,6\]

![](output_imgs/recolorized_train.jpeg)

### self\_portrait: Red \[175,37\], Green \[77,29\]

![](output_imgs/recolorized_self_portrait.jpeg)

### onion\_church: Red \[107,37\], Green \[49,26\]

![](output_imgs/recolorized_onion_church.jpeg)

### melons: Red \[179,13\], Green \[83,10\]

![](output_imgs/recolorized_melons.jpeg)

### workshop: Red \[106,-11\], Green \[53,0\]

![](output_imgs/recolorized_workshop.jpeg)

### emir: Red \[106,41\], Green \[48,23\]

![](output_imgs/recolorized_emir.jpeg)

### three\_generations: Red \[108,12\], Green \[49,15\]

![](output_imgs/recolorized_three_generations.jpeg)

### lady: Red \[108,11\], Green \[48,7\]

![](output_imgs/recolorized_lady.jpeg)

### icon: Red \[89,24\], Green \[40,18\]

![](output_imgs/recolorized_icon.jpeg)

### castle: Red \[97,5\], Green \[33,2\]

![](output_imgs/recolorized_castle.jpeg)

Extra Images
------------

### belaia: Red \[118,-34\], Green \[49,-16\]

![](output_imgs/recolorized_belaia.jpeg)

### perm: Red \[101,-35\], Green \[41,-19\]

![](output_imgs/recolorized_perm.jpeg)

### stone: Red \[78,8\], Green \[30,6\]

![](output_imgs/recolorized_stone.jpeg)