from functools import reduce

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


def xor(image_path: str, key_path: str) -> np.ndarray:
    image = read_image(image_path)
    key_image = read_image(key_path)

    flat_key = key_image.reshape(-1)
    flat_key = resize_flat(flat_key, reduce(lambda a, b: a * b, image.shape))
    key = flat_key.reshape(image.shape)
    result: np.ndarray = image ^ key
    return result


def read_image(path: str) -> np.ndarray:
    def _read_png() -> np.ndarray:
        image: np.ndarray = mpimg.imread(path)
        image = image * 255
        image = image.astype(np.uint8)
        image = np.delete(image, -1, axis=2)
        return image

    def _read_jpg() -> np.ndarray:
        image: np.ndarray = mpimg.imread(path, format=format)  # type: ignore
        return image

    format = path.split(".")[-1]
    # match format:
    #     case "jpg" | "jpeg":
    #         return _read_jpg()
    #     case "png":
    #         return _read_png()
    # raise Exception
    if format == "jpg" or format == "jpeg":
        return _read_jpg()
    elif format == "png":
        return _read_png()
    raise Exception


def resize_flat(array: np.ndarray, target_len: int) -> np.ndarray:
    current_size = array_size = len(array)
    result: np.ndarray = array.copy()

    if current_size > target_len:
        return result[:target_len]  # type: ignore

    while current_size < target_len:
        difference = target_len - current_size
        if array_size < difference:
            result = np.append(result, array)
        else:
            result = np.append(result, array[:difference])
        current_size = len(result)
    return result


def save(path: str, image: np.ndarray) -> str:
    def _save() -> None:
        plt.imsave(path, image, format="PNG")  # type: ignore

    if path.endswith(".png"):
        _save()
        return path
    elif path.endswith(".jpg") or path.endswith(".jpeg"):
        path = path.removesuffix(".jpg")
        path = path.removesuffix(".jpeg")
    path = path + ".png"
    _save()
    return path
