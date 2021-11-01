import time
from typing import Any


class Timer:
    def __init__(self) -> None:
        self.start_time: float = 0.0

    def __enter__(self) -> None:
        self.start_time = time.perf_counter()

    def __exit__(self, *_: Any, **__: Any) -> None:
        elapsed_time = time.perf_counter() - self.start_time
        print()
        print("Took {:0.4f} seconds".format(elapsed_time))
