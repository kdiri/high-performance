"""
Basic caching and also lru_cache examples

Execution times to get fibonacci number of 30

| ------ No cache
Time elapsed: 3.203935502
| ------ With lru cache
Time elapsed: 2.995000000005632e-05
| ------ With memory cache
Time elapsed: 0.012280038999999299


"""
from time import perf_counter, time
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

    #@time_decorator
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


class FactClass2:
    def __init__(self):
        self.cache: dict = {}

    def __call__(self, num):
        if num < 0:
            raise ValueError
        if num not in self.cache:
            product: int = 1
            for i in range(num):
                if i not in self.cache:
                    self.cache[i] = product
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


def process_fact_classes():
    cached_class = FactClass()
    cached_class2 = FactClass2()
    print("| ------ With V1")
    start = time()
    for i in range(100000, 1, -1):
       cached_class(i)
    print(f"Time elapsed for V1: {time() - start}")
    print("| ------ With V2")
    start = time()
    for i in range(100000, 1, -1):
        cached_class2(i)
    print(f"Time elapsed for V2: {time() - start}")


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
        fibonacci_simple(30)


@time_decorator
def process_fibo_cache():
    print("| ------ With lru cache")
    for i in range(5):
        fibonacci_cache(30)


@time_decorator
def process_fibo_mem_cache():
    print("| ------ With memory cache")
    for i in range(5):
        fibonacci_mem_cache(30)


def process():
    process_fibo_simple()
    process_fibo_cache()
    #process_fibo_mem_cache()
    #process_basic_caches()
    #process_fact_classes()


if __name__ == "__main__":
    process()
