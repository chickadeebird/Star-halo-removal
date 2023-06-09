import numpy as np
import tifffile
from scipy import ndimage
from skimage.draw import circle_perimeter
from astropy.io import fits
import matplotlib.pyplot as plt

DISPLAY_IMAGES = False

base_dir = 'Polaris/'

stars_filename = base_dir + '/Polaris Lumdenoised16.fit'

hdu_list = fits.open(stars_filename)
lum_image = hdu_list[0].data

# Sadr x 710 y 1418
x_centre = 1296
y_centre = 856

# radius = x_centre - 100
# Sadr 600
radius = 850
# radius = 128

if DISPLAY_IMAGES:
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    cmap = plt.cm.gray
    ax1.imshow(lum_image, cmap=cmap)
    # ax2 = fig.add_subplot(1, 2, 2)
    # ax2.imshow(median_B, cmap=cmap)
    plt.show()

line_lum = lum_image[y_centre,x_centre-radius:x_centre+radius]
# line_G = G[y_centre,x_centre-radius:x_centre+radius]
# line_B = B[y_centre,x_centre-radius:x_centre+radius]

filter_size = 51
filter_size = 3

median_lum = ndimage.median_filter(line_lum, filter_size)


subimage_lum = lum_image[y_centre-radius:y_centre+radius,x_centre-radius:x_centre+radius]


if DISPLAY_IMAGES:
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    cmap = plt.cm.gray
    ax1.imshow(subimage_lum, cmap=cmap)

    plt.show()

# G[y_centre-radius:y_centre+radius,x_centre-radius:x_centre+radius] = subimage_new_G[:,:]
# B[y_centre-radius:y_centre+radius,x_centre-radius:x_centre+radius] = subimage_new_B[:,:]

def create_cone(subimage, cone_radius):
    cone_image = np.zeros(subimage.shape,dtype=float)

    # cur_dil_image[radius,radius] = 1.
    final_median = 0.
    # prev_median = 0.

    for rad in range(cone_radius):
        # next_dil_image = dilation(cur_dil_image)
        # ring_dil_image = (next_dil_image - cur_dil_image).astype(bool)
        rr, cc = circle_perimeter(cone_radius, cone_radius, rad)
        ring_dil_image = np.ones(subimage.shape, dtype=bool)
        ring_dil_image[rr, cc] = False

        ring_mask = np.ma.array(subimage, mask=ring_dil_image)
        ring_median = np.ma.median(ring_mask)

        final_median = ring_median

        new_median_ring = ring_median * (1. - ring_dil_image.astype(float))

        cone_image = np.maximum(new_median_ring, cone_image)

        # cur_dil_image = next_dil_image

        a=1

    filter_size = 5
    cone_image = ndimage.median_filter(cone_image, filter_size)
    cone_image = cone_image - final_median
    cone_image = cone_image.clip(min=0)

    return cone_image

cone_image_lum = create_cone(subimage_lum, radius)

if DISPLAY_IMAGES:
    fig = plt.figure()
    cmap = plt.cm.gray
    ax1 = fig.add_subplot(3, 3, 1)
    ax1.imshow(subimage_lum, cmap=cmap)
    ax2 = fig.add_subplot(3, 3, 2)
    ax2.imshow(cone_image_lum, cmap=cmap)
    ax3 = fig.add_subplot(3, 3, 3)
    ax3.imshow(subimage_lum - cone_image_lum, cmap=cmap)

    plt.show()

power_factor = 10
max_cone_lum = np.max(cone_image_lum)
replace_Sadr = cone_image_lum.astype(float) ** power_factor
max_replace_Sadr = np.max(replace_Sadr)
replace_Sadr = replace_Sadr * max_cone_lum / max_replace_Sadr

lum_image[y_centre-radius:y_centre+radius,x_centre-radius:x_centre+radius] = (subimage_lum.astype(float) - cone_image_lum.astype(float) + replace_Sadr).clip(min=0, max=65535).astype(int)[:,:]

save_path = base_dir + '/Polaris Lumdenoised16 halo removed.fit'

hdu_list[0].data = lum_image
hdu_list.writeto(save_path)

print('Done')