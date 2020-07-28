

# demonstrate stacking

import numpy as np
import matplotlib.pyplot as plt
from photutils import detect_sources


# --- function to detect sources (see below for context)

def detect(sci, wht):

    noise = 1/np.sqrt(wht) # noise map
    sig = sci/noise # significance map

    # --- detect sources via segmentation
    threshold = 2.5
    npixels = 5

    try:

        segm = detect_sources(sig, threshold, npixels=npixels) # make segmentation image

        signal = np.sum(sci[np.where(segm.data==1)])
        print(f'the signal is: {signal}')

        error = np.sqrt(np.sum(noise[np.where(segm.data==1)]**2))
        print(f'the error (noise) is: {error}')
        
        print(f'the signal-to-noise is: {signal/error}')

    except:

        print('no sources detected')






# --- vmin/vmax for plotting images
vmin = -10
vmax = 10

# --- for use when making significance images
threshold = 2

# --- size of image
size = 50

# --- create a 2D gaussian source
x, y = np.meshgrid(range(size), range(size))
x_c = 35 # x-centre
y_c = 35 # y-centre
sigma = 2 # width of gaussian
A = 5 # amplitude
source = A*np.exp(-( ((x-x_c)**2 + (y-y_c)**2)  / (2.0*sigma**2 ) ) ) # 2D gaussian

# --- show the source
plt.imshow(source, cmap = 'magma', vmin = 0, vmax = vmax)
plt.axis('off')
plt.show()



# Now we are going to create 5 individual images containing both the source and noise

# --- define the background in each individiual frame. This is the \sigma of the gaussian random noise we'll put in. Note that this is much higher for the final frame
bkg_values = [1.,1.,1.,1.,5.]


s = (len(bkg_values), size, size) # define a numpy array containing all frames.
sci = np.zeros(s) # science frames. The first frame would be sci[0] etc.
wht = np.ones(s) # wht frames


# --- create the science and why frames
for i, bkg_value in enumerate(bkg_values):
    wht[i] *= 1/bkg_value**2 # just uniform weight image
    sci[i] = bkg_value*np.random.randn(size, size) # make gaussian random background
    sci[i] += source # add in source

    # --- detect sources
    print(f'---- frame {i}: bkg = {bkg_value}')
    detect(sci[i], wht[i])


# --- plot both the science frame and the significance (science/noise) image

fig, axes = plt.subplots(2, len(bkg_values), figsize = (2*len(bkg_values), 4))
for i in range(len(bkg_values)):

    # --- plot the image
    axes[0, i].imshow(sci[i], cmap = 'magma', vmin = vmin, vmax = vmax)
    axes[0, i].axis('off')

    # --- significance map
    sig = sci[i]*np.sqrt(wht[i]) # this is the same as sci/noise

    # --- plot the significance map
    axes[1, i].imshow(sig, vmin = -threshold, vmax = threshold, cmap = 'Greys')
    axes[1, i].imshow(np.ma.masked_where(sig <= threshold, sig), cmap = 'plasma', vmin = threshold, vmax = 50)
    axes[1, i].axis('off')

plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0.01)
plt.show()




# --- naively stack science images
csci = np.sum(sci, axis=0)/len(bkg_values)
cwht = np.sum(wht, axis=0)/len(bkg_values)

sig = csci*np.sqrt(cwht) # this is the same as sci/noise

# --- plot the significance map
plt.imshow(sig, vmin = -threshold, vmax = threshold, cmap = 'Greys')
plt.imshow(np.ma.masked_where(sig <= threshold, sig), cmap = 'plasma', vmin = threshold, vmax = 50)
plt.axis('off')
plt.show()

# --- detect sources
print()
print('---- naive stack')
detect(csci, cwht)


# --- properly stack science images


# -- long way
# csci = np.zeros((size,size))
# cwht = np.zeros((size,size))
# for i in range(len(bkg_values)):
#     csci += sci[i]*wht[i]
#     cwht += wht[i]
# csci /= cwht

# -- short way
cwht = np.sum(wht, axis=0)
csci = np.sum(sci*wht, axis=0)/cwht

sig = csci*np.sqrt(cwht)

# --- plot the significance map
plt.imshow(sig, vmin = -threshold, vmax = threshold, cmap = 'Greys')
plt.imshow(np.ma.masked_where(sig <= threshold, sig), cmap = 'plasma', vmin = threshold, vmax = 50)
plt.axis('off')
plt.show()

# --- detect sources
print()
print('---- weighted stack')
detect(csci, cwht)
