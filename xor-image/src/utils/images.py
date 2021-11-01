from pathlib import Path


def get_images_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "images"
