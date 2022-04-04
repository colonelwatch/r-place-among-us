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
        # we won't care about pixels marked -1 on the stencil
        self.where_part0 = np.where(stencil == 0)
        self.where_part1 = np.where(stencil == 1)
        self.where_part2 = np.where(stencil == 2)
    def check(self, slice):
        part0 = slice[self.where_part0]
        part1 = slice[self.where_part1]
        if any(part1[0] != part1) or any(part1[0] == part0):
            return False
        part2 = slice[self.where_part2]
        if any(part2[0] != part2) or any(part2[0] == part0) or part1[0] == part2[0]:
            return False
        return True # color in part1 and part2 are consistent, and they don't match with part0 or each other

amongus1 = StencilMatcher([
    [ 0, 1, 1, 1, 0],
    [-1, 1, 2, 2, 0],
    [-1, 1, 1, 1, 0],
    [-1,-1, 1, 1,-1],
    [ 0, 1, 0, 1, 0]
])
amongus2 = StencilMatcher([
    [ 0, 1, 1, 1, 0],
    [ 0, 2, 2, 1,-1],
    [ 0, 1, 1, 1,-1],
    [-1, 1, 1,-1,-1],
    [ 0, 1, 0, 1, 0]
])
amongus3 = StencilMatcher([
    [ 0, 1, 1, 1, 0],
    [-1, 1, 2, 2, 0],
    [-1,-1, 1, 1,-1],
    [ 0, 1, 0, 1, 0]
])
amongus4 = StencilMatcher([
    [ 0, 1, 1, 1, 0],
    [ 0, 2, 2, 1,-1],
    [-1, 1, 1,-1,-1],
    [ 0, 1, 0, 1, 0]
])


sus = np.zeros_like(x_paletted)
for i in range(2000):
    for j in range(2000):
        try: # these should be try-excepted individually
            x_slice = x_paletted[i:i+amongus1.rows, j:j+amongus1.cols]
            sus[i, j] = sus[i, j] or amongus1.check(x_slice)
            x_slice = x_paletted[i:i+amongus2.rows, j:j+amongus2.cols]
            sus[i, j] = sus[i, j] or amongus2.check(x_slice)
            x_slice = x_paletted[i:i+amongus3.rows, j:j+amongus3.cols]
            sus[i, j] = sus[i, j] or amongus3.check(x_slice)
            x_slice = x_paletted[i:i+amongus4.rows, j:j+amongus4.cols]
            sus[i, j] = sus[i, j] or amongus4.check(x_slice)
        except IndexError:
            continue

i, j = np.where(sus)
x, y = j+2.5, i+2.5 # maps from ij coords to imshow coords, and centers markers
plt.scatter(x, y, color='cyan', marker='x')

print(len(i)) # prints the # among us

plt.savefig("Figure_1.png", dpi=600)