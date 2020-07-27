

import numpy as np

# --- define an array of 10 numbers from 1 to 10
a = np.linspace(1,10,10)
# Out[4]: array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])


# --- define a selection array "s" using "a". When the condition is met the element is True
s1 = a > 4
# Out[8]: array([False, False, False, False,  True,  True,  True,  True,  True, True])


# --- apply the selection array "s" to "a" and create a new array "b"
b = a[s1]
# Out[7]: array([ 5.,  6.,  7.,  8.,  9., 10.])

# --- define a second selection array
s2 = a < 9.

# --- combine with s1
s3 = s1 & s2 # logical AND

# --- apply to a
c = a[s3]
# Out[2]: array([5., 6., 7., 8.])


# --- now lets demonstrate the logical OR

s4 = a < 5
s5 = a > 8
s6 = s4 | s5 # logical OR

d = a[s6]
# Out[7]: array([ 1.,  2.,  3.,  4.,  9., 10.])


# --- the "~" reverses the selection

e = a[~s6]
# Out[9]: array([5., 6., 7., 8.])
