


# --- In this example we simply carry out a conversion from signal (e/s) to flux. In this case we simply assume the same signal in every band.

import numpy as np


nJy_to_es = {'f435w': 0.005171303179169625, 'f606w': 0.011015393095414123, 'f775w': 0.005142804319487919, 'f814w': 0.0066619290022345385, 'f850lp': 0.0024366884234595892, 'f105w': 0.008863392873279346, 'f125w': 0.008550667128846823, 'f140w': 0.010490592077764458, 'f160w': 0.006582638416409025}

filters = ['f435w','f606w', 'f775w','f814w', 'f850lp', 'f105w','f125w','f140w','f160w']


signal = 0.01 # e/s

for f in filters:
    print(f'flux/nJy: {signal/nJy_to_es[f]}')
