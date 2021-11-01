""""
Compare numba compiler with pypy

sum_sq
| ------ No JIT compiler
Time elapsed: 0.024084642999999906
Time elapsed: 0.047137176
Time elapsed: 0.025227007999999995
Time elapsed: 0.024629856000000006
Time elapsed: 0.02448545099999999
| ------ With Numba JIT compiler
Time elapsed: 0.5215501619999999
Time elapsed: 0.3916337700000001
Time elapsed: 0.45751048299999986
Time elapsed: 0.4688111130000001
Time elapsed: 0.40204395700000006

------------------------------------------
monte_carlo_pi

| ------ No JIT compiler
Time elapsed: 4.5762821140000005
3.1414692
| ------ With JIT compiler
Time elapsed: 0.5371958600000006
3.1414752

-----------------------------------------
Numpy - Numba
| ------ Vectorize inside of function
Time elapsed: 12.332058748000001

| ------ Numpy Vectorize as a decorator
Time elapsed: 11.061957823999997

| ------ Numba Vectorize as a decorator
Time elapsed: 1.1217202250000007

"""
from typing import List
from numba import jit, vectorize
import numpy as np
from high_perf.caching import time_decorator
import random


# Numpy vectorize as a decorator
@time_decorator
@np.vectorize
def cantor_deco(a, b):
    return int(0.5 * (a + b) * (a + b + 1) + b)


# Numba vectorize as a decorator
@time_decorator
@vectorize(nopython=True)
def cantor_deco_numba(a, b):
    return int(0.5 * (a + b) * (a + b + 1) + b)


def apply_math_func(a, b):
    return int(0.5 * (a + b) * (a + b + 1) + b)


@time_decorator
def cantor_normal(a, b):
    return np.vectorize(apply_math_func)(a, b)


@time_decorator
def monte_carlo_pi(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples


@time_decorator
@jit
def monte_carlo_pi_jit(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples


@time_decorator
def sum_sq(elements: List[int]) -> int:
    res: int = 0
    for i, element in enumerate(elements):
        res += element ^ 2
    return res


@time_decorator
@jit(fastmath=True)
def sum_sq_numba(elements: List[int]) -> int:
    res: int = 0
    for i, element in enumerate(elements):
        res += element ^ 2
    return res


def process():
    list_to_send = [x for x in range(1, 222903)]
    print("| ------ No JIT compiler")
    for x in range(5):
        sum_sq(list_to_send)
    print("| ------ With JIT compiler")
    for x in range(5):
        sum_sq_numba(list_to_send)


def process_monte_carlo():
    print("| ------ No JIT compiler")
    print(monte_carlo_pi(10_000_000))
    print("| ------ With JIT compiler")
    print(monte_carlo_pi_jit(10_000_000))


def process_no_vectorize():
    list_to_send = [x for x in range(1, 22290398)]
    print("| ------ Vectorize inside of function")
    print(cantor_normal(list_to_send, 2))
    print("| ------ Numpy Vectorize as a decorator")
    print(cantor_deco(np.array(list_to_send), 2))
    print("| ------ Numba Vectorize as a decorator")
    print(cantor_deco_numba(np.array(list_to_send), 2))


if __name__ == "__main__":
    process_no_vectorize()
