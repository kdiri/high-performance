from time import perf_counter


def time_decorator(fn):
    """
    Decorator to time a function
    :param fn:
    :return:
    """
    def inner(*args):
        start = perf_counter()
        result = fn(*args)
        end = perf_counter()
        print(f"Time elapsed: {end - start}")
        return result

    return inner


def recur_factorial(num: int) -> int:
    """
    Recursive function to find the factorial of a number.
    :param num:
    :return:
    """
    if num <= 0:
        return 1
    return num * recur_factorial(num-1)


#@time_decorator
def calc_factorial(num: int) -> int:
    """
    Calculate factorial
    :param num:
    :return: product of all numbers from 1 to num
    """
    if num < 0:
        raise ValueError
    product: int = 1
    for i in range(num):
        product = product * (i + 1)
    return product


@time_decorator
def method_to_call_recursive_function(num: int):
    return recur_factorial(num)


if __name__ == '__main__':
    #print(calc_factorial(750))
    print(method_to_call_recursive_function(750))
    #print(calc_factorial(7500))
    #print(method_to_call_recursive_function(7500))
