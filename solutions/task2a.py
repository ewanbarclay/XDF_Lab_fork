

import numpy as np
from astropy.io import fits

save = True

# --- create a near-IR detection image by combining (stacking) a list of images together

image_dir = '../data' # image directory relative to this script

filters = ['f105w','f125w','f140w','f160w'] # list of images to combine (stack)

sci = {f: fits.getdata(f'{image_dir}/{f}_sci.fits') for f in filters} # read sci images
wht = {f: fits.getdata(f'{image_dir}/{f}_wht.fits') for f in filters} # read weight images


shape = next(iter(sci.values())).shape
combined_sci = np.zeros(shape)
combined_wht = np.zeros(shape)

for f in filters:
    combined_sci += sci[f] * wht[f]
    combined_wht += wht[f]

combined_sci /= combined_wht

if save:

    np.save('data/detection_sci.npy', combined_sci)
    np.save('data/detection_wht.npy', combined_wht)
