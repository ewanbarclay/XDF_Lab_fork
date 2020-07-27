


# --- In this example we look at some more properties of the sources identified by segmentation.


import numpy as np
from astropy.io import fits

image_dir = '../data' # define image directory relative to this script

f = 'f125w' # filter

sci = fits.getdata(f'{image_dir}/{f}_sci.fits') # read science FITS file data into numpy array
wht = fits.getdata(f'{image_dir}/{f}_wht.fits') # read weight FITS file data into numpy array

mask = fits.getdata(f'{image_dir}/mask.fits') # read in the image mask
sci = np.ma.masked_array(sci, mask = mask) # apply the mask to our science image
wht = np.ma.masked_array(wht, mask = mask) # apply the mask to our weight image

# --- cut out a portion of the image for analysis

x = 2500 # pixel x-centre of cutout, must be an integer
y = 2500 # pixel y-centre of cutout, must be an integer
r = 100 # width/2 of cutout, must be int

sci = sci[x-r:x+r, y-r:y+r] # cutout a portion of the science image
wht = wht[x-r:x+r, y-r:y+r] # cutout a portion of the weight image

# --- define the noise in each pixel and make a significance map (signal/noise)

noise = 1./np.sqrt(wht) # conversion from weight to noise
sig = sci/noise # signifance map



# --- now run segmentation on the image to detect sources.

from photutils import detect_sources


threshold = 2.5 # require each pixel have a significance of >2.5 (since we're using the significance image)
npixels = 5 # require at least 5 connected pixels

segm = detect_sources(sig, threshold, npixels=npixels) # make segmentation image


# --- get various properties of the sources, crucially inclusing their centres

from photutils import source_properties, CircularAperture

cat = source_properties(sci, segm)


# --- get a list of positions (x,y) of the sources

positions = []
for obj in cat:
    positions.append(np.transpose((obj.xcentroid.value, obj.ycentroid.value)))

# --- make a CicrcularAperture object. This can be plotted but is mostly used for the aperture photometry.

r = 5. # radius of aperture in pixels
apertures = CircularAperture(positions, r)

# --- let's make a plot of the sources and the apertures

import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12.5))
ax1.imshow(sci, origin='lower', cmap='Greys_r')
ax1.set_title('Science')
cmap = segm.make_cmap(random_state=12345)
ax2.imshow(segm, origin='lower', cmap=cmap)
ax2.set_title('Segmentation Image')
for aperture in apertures:
    aperture.plot(axes=ax1, color='white', lw=1.5)
    aperture.plot(axes=ax2, color='white', lw=1.5)
plt.show()


# --- now let's do some photometry

from photutils import aperture_photometry

phot_table = aperture_photometry(sci, apertures)
phot_table['aperture_sum'].info.format = '%.8g'  # for consistent table output
print(phot_table)
