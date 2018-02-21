# See: https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
from skimage import data
import matplotlib.pyplot as plt
import numpy as np
import itertools
from PIL import Image, ImageDraw

# Import some data
check = data.checkerboard()
#plt.imshow(check, cmap="gray")

# Convert to PIL image
imcheck = Image.fromarray(check)
imdraw = ImageDraw.Draw(imcheck)
#imcheck.show()

# Add number in each case of checkerboard
# Position of centers
centers = np.arange(12, 190, 25)
ncase = 0
for pair in itertools.product(centers, centers):
    # white case
    if check[pair] >= 128:
        imdraw.text(pair, str(ncase), fill=0)
    # black case
    else:
        imdraw.text(pair, str(ncase), fill = 256)
    ncase += 1

imcheck.save('temp.jpg')
