


# --- In this example we look at the properties of one of the sources identified by segmentation.


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



# --- now run segmentation on the image.

from photutils import detect_sources
import matplotlib.pyplot as plt


threshold = 2.5 # require each pixel have a significance of >2.5 (since we're using the significance image)
npixels = 5 # require at least 5 connected pixels

segm = detect_sources(sig, threshold, npixels=npixels) # make segmentation image

plt.imshow(segm, cmap = 'rainbow') # plot masked segmentation map
plt.show()


# --- calculate object positions

from photutils import source_properties

cat = source_properties(sci, segm)
positions = [np.transpose((obj.xcentroid.value, obj.ycentroid.value)) for obj in cat]


# --- display single object

i = 8

mask = ~((segm.data==i)|(segm.data==0)) # only background + object
# mask = segm.data!=i # only object
masked_segm = np.ma.array(segm, mask = mask) # mask all pixels except object i

plt.imshow(masked_segm, cmap = 'rainbow') # plot masked segmentation map
plt.show()

from photutils import CircularAperture

radii = np.arange(1,21,1)
apertures = [CircularAperture(positions[i-1], r=r) for r in radii]

from photutils import aperture_photometry

phot_table = aperture_photometry(sci, apertures, mask = mask)
print(phot_table)
