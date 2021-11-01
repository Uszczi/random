import click
from functools import reduce

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

image = mpimg.imread("orginal.jpg", format="jpg")

# image = Image.open("encrypted.png")
# image = np.array(image)
# image = np.delete(image, -1, axis=2)


flat_image = image.reshape(-1)

key = mpimg.imread("key.jpeg", format="jpeg")
key_flat = key.reshape(-1)
key_flat_copy = key_flat.copy()

target_size = reduce(lambda a, b: a * b, image.shape)
current_size = key_size = len(key_flat)


while current_size < target_size:
    difference = target_size - current_size
    if key_size < difference:
        key_flat = np.append(key_flat, key_flat_copy)
    else:
        key_flat = np.append(key_flat, key_flat_copy[:difference])
    current_size = len(key_flat)


key_reshaped = key_flat.reshape(image.shape)

xor = image ^ key_reshaped

# plt.imshow(xor)
# plt.show()

plt.imsave("encrypted.png", xor, format="PNG")
