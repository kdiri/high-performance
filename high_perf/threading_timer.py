import time


class Timer:
    def __init__(self, timeout):
        self.timeout = timeout
        self.start = time.time()

    def done(self):
        return time.time() - self.start > self.timeout


def process():
    timer = Timer(1.0)
    while True:
        if timer.done():
            print("Timer is done")
            break


if __name__ == "__main__":
    process()
