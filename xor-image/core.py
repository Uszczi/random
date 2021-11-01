from ctypes import resize
from functools import reduce

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def xor(image_path, key_path) -> np.array:
    image = read_image(image_path)
    key_image = read_image(key_path)
    flat_key = key_image.reshape(-1)

    flat_key = resize_flat(flat_key, reduce(lambda a,b: a * b, image.shape))
    key = flat_key.reshape(image.shape)
    result = image ^ key

    # plt.imsave("encrypted.png", result, format="PNG")
    return result


def read_image(path: str):
    def _read_png():
        image = Image.open(path)
        image = np.array(image)
        image = np.delete(image, -1, axis=2)
        return image

    def _read_jpg():
        image = mpimg.imread(path, format=format)
        return image

    format = path.split(".")[-1]
    match format:
        case "jpg" | "jpeg":
            return _read_jpg()
        case "png":
            return _read_png()



def resize_flat(array, target_len):
    current_size = array_size = len(array)
    result = array.copy()

    if current_size > target_len:
        return result[:target_len]


    while current_size < target_len:
        difference = target_len - current_size
        if array_size < difference:
            result = np.append(result, array)
        else:
            result = np.append(result, array[:difference])
        current_size = len(result)
    return result
