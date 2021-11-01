import time


class Timer:
    def __init__(self) -> None:
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()

    def __exit__(self, *_, **__):
        elapsed_time = time.perf_counter() - self.start_time
        print()
        print("Took {:0.4f} seconds".format(elapsed_time))
