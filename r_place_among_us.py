from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

# local r/place copy taken from web browser comes in four pieces
x_ul = Image.open('2022placeul.png').convert('RGB')
x_ur = Image.open('2022placeur.png').convert('RGB')
x_dl = Image.open('2022placedl.png').convert('RGB')
x_dr = Image.open('2022placedr.png').convert('RGB')

x = np.empty((2000, 2000, 3), dtype=np.uint8)
x[:1000, :1000] = np.array(x_ul)
x[:1000, 1000:] = np.array(x_ur)
x[1000:, :1000] = np.array(x_dl)
x[1000:, 1000:] = np.array(x_dr)

plt.imshow(x)

x_flattened = x.reshape(2000*2000, 3)
x_flattened_tupled = [tuple(pixel) for pixel in x_flattened]

palette = sorted(set(x_flattened_tupled)) # extracts the palette
x_paletted = np.array([palette.index(pixel) for pixel in x_flattened_tupled]).reshape(2000, 2000)

class StencilMatcher:
    def __init__(self, stencil):
        stencil = np.array(stencil)
        self.rows = stencil.shape[0]
        self.cols = stencil.shape[1]
        self.n_parts = np.max(stencil)+1
        self.where = [np.where(stencil == i) for i in range(self.n_parts)]
    def check(self, slice):
        parts = [slice[where_i] for where_i in self.where]
        for i in range(self.n_parts):
            if any(parts[i][0] != parts[i]) and i != 0: # inconsistency check (0 is exempt)
                return False
            if any([parts[i][0] in parts[j] for j in range(i)]): # match check
                return False
        return True

# -1 means we don't care
# 0 means it shouldn't match with 1,2,3,.. but we don't care about consistency
# 1,2,3,... means we care about consistency AND no matching
amongi = [
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [-1, 1, 2, 2, 0],
        [-1, 1, 1, 1, 0],
        [-1,-1, 1, 1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [ 0, 2, 2, 1,-1],
        [ 0, 1, 1, 1,-1],
        [-1, 1, 1,-1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [-1, 1, 2, 2, 0],
        [-1,-1, 1, 1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [ 0, 2, 2, 1,-1],
        [-1, 1, 1,-1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [-1, 1, 2, 3, 0],
        [-1, 1, 1, 1, 0],
        [-1,-1, 1, 1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [ 0, 3, 2, 1,-1],
        [ 0, 1, 1, 1,-1],
        [-1, 1, 1,-1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [-1, 1, 2, 3, 0],
        [-1,-1, 1, 1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
    StencilMatcher([
        [ 0, 1, 1, 1, 0],
        [ 0, 3, 2, 1,-1],
        [-1, 1, 1,-1,-1],
        [ 0, 1, 0, 1, 0]
    ]),
]

sus = np.zeros_like(x_paletted)
for i in range(2000):
    for j in range(2000):
        for amongus in amongi:
            try: # these should be try-excepted individually
                x_slice = x_paletted[i:i+amongus.rows, j:j+amongus.cols]
                sus[i, j] = sus[i, j] or amongus.check(x_slice)
            except IndexError:
                continue

i, j = np.where(sus)
x, y = j+2.5, i+2.5 # maps from ij coords to imshow coords, and centers markers
plt.scatter(x, y, color='cyan', marker='x')

print(len(i)) # prints the # among us

plt.savefig("Figure_1.png", dpi=600)