# Use this script to annotate keypoints on an image
import argparse
import csv
import os
import matplotlib.pyplot as plt
import skimage.io as skio

parser = argparse.ArgumentParser(description='Keypoint annotation script.')
parser.add_argument('imgpath', type=str, help='Path to the img')
parser.add_argument('-n', type=int, default=10, help='Number of points to annotate')
parser.add_argument('-s', type=str, default="", help='output file suffix')

args = parser.parse_args()
n_points = args.n
img_path = args.imgpath
out_suffix = args.s

img_filename = os.path.splitext(os.path.basename(img_path))[0]

image = skio.imread(img_path)
plt.imshow(image)
points = plt.ginput(n_points, timeout=0, show_clicks=True)
plt.close()

csv_path = os.path.join(os.path.dirname(img_path), f'{img_filename}{out_suffix}.csv')

with open(csv_path, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(points)