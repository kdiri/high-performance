"""
Basic caching and also lru_cache examples
"""
from time import perf_counter
from functools import lru_cache
from joblib import Memory

memory = Memory("/Users/kdiri/github/cachedir")


def time_decorator(fn):
    def inner(*args):
        start = perf_counter()
        result = fn(*args)
        end = perf_counter()
        print(f"Time elapsed: {end - start}")
        return result

    return inner


@time_decorator
def calc_factorial(num):
    """
    No cache
    :param num:
    :return:
    """
    if num < 0:
        raise ValueError
    product: int = 1
    for i in range(num):
        product = product * (i + 1)
    return product


class FactClass:
    def __init__(self):
        self.cache: dict = {}

    @time_decorator
    def __call__(self, num):
        if num < 0:
            raise ValueError
        if num not in self.cache:
            product: int = 1
            for i in range(num):
                product = product * (i + 1)
            self.cache[num] = product
            return self.cache[num]
        return self.cache[num]


def process_basic_caches():
    cached_class = FactClass()
    print("| ------ No cache")
    for i in range(5):
        calc_factorial(100000)
    print("| ------ With cache")
    for i in range(5):
        cached_class(100000)


def fibonacci_simple(num):
    if num < 1:
        return 1
    return fibonacci_simple(num - 1) + fibonacci_simple(num - 2)


@lru_cache(maxsize=None)
def fibonacci_cache(num):
    if num < 1:
        return 1
    return fibonacci_cache(num - 1) + fibonacci_cache(num - 2)


@memory.cache
def fibonacci_mem_cache(num):
    if num < 1:
        return 1
    return fibonacci_mem_cache(num - 1) + fibonacci_mem_cache(num - 2)


@time_decorator
def process_fibo_simple():
    print("| ------ No cache")
    for i in range(5):
        fibonacci_simple(20)


@time_decorator
def process_fibo_cache():
    print("| ------ With cache")
    for i in range(5):
        fibonacci_cache(20)


@time_decorator
def process_fibo_mem_cache():
    print("| ------ With memory cache")
    for i in range(5):
        fibonacci_mem_cache(50)


def process():
    process_fibo_simple()
    process_fibo_cache()
    process_fibo_mem_cache()


if __name__ == "__main__":
    process()
