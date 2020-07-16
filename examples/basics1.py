

import numpy as np



# --- define an array of 10 numbers from 1 to 10
a = np.linspace(1,10,10)
# Out[4]: array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])


# --- define a selection array "s" using "a". When the condition is met the element is True
s = a > 4
# Out[8]: array([False, False, False, False,  True,  True,  True,  True,  True, True])


# --- apply the selection array "s" to "a" and create a new array "b"
b = a[s]
# Out[7]: array([ 5.,  6.,  7.,  8.,  9., 10.])
