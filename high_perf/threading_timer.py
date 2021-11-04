import time


class Timer:
    def __init__(self, timeout):
        self.timeout = timeout
        self.start = time.time()

    def done(self):
        return time.time() - self.start > self.timeout

    def on_timer_done(self, callback):
        self.callback = callback


def process():
    timers = []
    timer1 = Timer(1.0)
    timer1.on_timer_done(lambda: print("First timer is done!"))
    timer2 = Timer(2.0)
    timer2.on_timer_done(lambda: print("Second timer is done!"))
    timers.append(timer1)
    timers.append(timer2)

    while timers:
        for timer in timers:
            if timer.done():
                timer.callback()
                timers.remove(timer)


if __name__ == "__main__":
    process()
