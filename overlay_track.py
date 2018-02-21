# See: https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
from skimage import data
import matplotlib.pyplot as plt
import numpy as np
import itertools
from PIL import Image, ImageDraw, ImageFont

# Import some data
check = data.checkerboard()  # greyscale
astro = data.astronaut()     # RGB
#plt.imshow(check, cmap="gray")

# Convert to PIL image
imcheck = Image.fromarray(check)
drawcheck = ImageDraw.Draw(imcheck)
fntcheck = ImageFont.truetype(font='arial', size=10)
#imcheck.show()
imastro = Image.fromarray(astro)
drawastro = ImageDraw.Draw(imastro)
fntastro = ImageFont.truetype(font='arial', size=25)

# ---------------------------------------------------------------

# Add number in each case of checkerboard
# Position of centers
centers = np.arange(10, 190, 25)
ncase = 0
for pair in itertools.product(centers, centers):
    # white case
    if check[pair] >= 128:
        drawcheck.text(pair, str(ncase), fill=0, font=fntcheck)
    # black case
    else:
        drawcheck.text(pair, str(ncase), fill = 256, font=fntcheck)
    ncase += 1

imcheck.save('temp_check.jpg')

# ---------------------------------------------------------------

# Annotate Head of astronaut and Rocket
drawastro.text((226,63), 'Head', fill=(255,255,255), font=fntastro)
drawastro.text((350,195), 'Rocket', fill=(255,0,0), font=fntastro)
imastro.save('temp_astro.jpg')
