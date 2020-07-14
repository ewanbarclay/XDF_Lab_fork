


# --- In this example you will learn to approproately combine (stack) different images


import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

save = False

# --- combine (stack) a list of images together

image_dir = '../data' # image directory relative to this script

mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask

filters = ['f435w','f606w'] # list of images to combine (stack)

sci = {f: fits.getdata(f'{image_dir}/{f}_sci.fits') for f in filters} # read sci images
wht = {f: fits.getdata(f'{image_dir}/{f}_wht.fits') for f in filters} # read weight images


shape = next(iter(sci.values())).shape
combined_sci = np.zeros(shape)
combined_wht = np.zeros(shape)

for f in filters:
    combined_sci += sci[f] * wht[f]
    combined_wht += wht[f]


# --- NOTE: this image can be used "as-is" or saved as a numpy array and read in later. To read back in simply use "array = np.load(filename)"


if save:

    filename = '_'.join(filters)
    np.save(f'{filename}_sci.npy', combined_sci)
    np.save(f'{filename}_wht.npy', combined_wht)
