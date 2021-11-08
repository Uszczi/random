from functools import reduce

import matplotlib.image as mpimg  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np


def xor(image_path: str, key_path: str) -> np.ndarray:
    image = read_image(image_path)
    key_image = read_image(key_path)
    h, w, _ = image.shape
    key = resize_image(key_image, h, w)
    # Uncomment those lines to see resized image.
    # plt.imshow(key)
    # plt.show()
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


def resize_image(image: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    def _resize_by_axis(
        array: np.ndarray, result: np.ndarray, target: int, axis: int
    ) -> np.ndarray:
        actual_size = result.shape[axis]
        while target > actual_size:
            difference = target - actual_size
            if difference >= array.shape[axis]:
                result = np.append(result, array.copy(), axis=axis)
            else:
                copy = np.delete(array, slice(difference, array.shape[axis]), axis=axis)
                result = np.append(result, copy, axis=axis)
            actual_size = result.shape[axis]
        return result

    result = image.copy()
    if result.shape[0] > target_h:
        result = np.delete(result, slice(target_h, result.shape[0]), axis=0)
    if result.shape[1] > target_w:
        result = np.delete(result, slice(target_w, result.shape[1]), axis=1)

    result = _resize_by_axis(image, result, target_h, axis=0)
    result = _resize_by_axis(result, result, target_w, axis=1)
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
