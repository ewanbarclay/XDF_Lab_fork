

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

image_dir = '../data' # define image directory relative to this script


filters = ['f435w','f606w', 'f775w','f850lp', 'f105w','f125w','f140w','f160w']

for f in filters:

    wht = fits.getdata(f'{image_dir}/{f}_wht.fits') # read FITS file data into numpy array

    plt.imshow(wht, cmap = 'bone')
    plt.show()
