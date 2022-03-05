from typing import List
from numba import autojit
from high_perf.caching import time_decorator


@time_decorator
def sum_square(elements: List[int]) -> int:
    res: int = 0
    for i, element in enumerate(elements):
        res += element ^ 2
    return res


@time_decorator
@autojit
def sum_square_with_numba(elements: List[int]) -> int:
    res: int = 0
    for i, element in enumerate(elements):
        res += element ^ 2
    return res


def measure_square_calculation():
    list_to_send = [x for x in range(1, 99999)]
    print("| ------ No JIT compiler")
    for x in range(5):
        sum_square(list_to_send)
    print("| ------ With JIT compiler")
    for x in range(5):
        sum_square_with_numba(list_to_send)


if __name__ == '__main__':
    measure_square_calculation()
