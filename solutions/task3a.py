

import numpy as np
import matplotlib.pyplot as plt
import pickle


nJy_to_es = {'f435w': 0.005171303179169625, 'f606w': 0.011015393095414123, 'f775w': 0.005142804319487919, 'f850lp': 0.0024366884234595892, 'f105w': 0.008863392873279346, 'f125w': 0.008550667128846823, 'f140w': 0.010490592077764458, 'f160w': 0.006582638416409025}


filters = ['f435w','f606w', 'f775w','f850lp', 'f105w','f125w','f140w','f160w']

cat = pickle.load(open('data/cat.p', 'rb'))  # read in signal catalogue

fluxes = {f: cat[f'{f}_signal']/nJy_to_es[f] for f in filters} # convert to flux/nJy
errors = {f: cat[f'{f}_noise']/nJy_to_es[f] for f in filters}

r1 = fluxes['f105w']/fluxes['f125w'] # break colour (mag) - usually on y-axis
r2 = fluxes['f850lp']/fluxes['f105w'] # slope colour (mag) - usually on x-axis

plt.scatter(r1, r2)

# --- need to add errors using error propagation?


plt.xlim([-0.3,2])
plt.ylim([-0.3,2])
plt.show()
