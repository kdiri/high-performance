""""
Compare numba compiler with pypy

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


"""
from typing import List
from numba import jit
import numpy as np
from high_perf.caching import time_decorator


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


if __name__ == '__main__':
    process()
