import pytest
from high_perf.blog_ex import recur_factorial, calc_factorial


@pytest.mark.parametrize("n, expected", [
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (8, 40320),
    (25, 15511210043330985984000000),
    (30, 265252859812191058636308480000000),
    (40, 815915283247897734345611269596115894272000000000),
    (50, 30414093201713378043612608166064768844377641568960512000000000000),
])
def test_recur_factorial(n, expected, benchmark):
    res = benchmark.pedantic(recur_factorial, args=(n,))
    assert expected == res


@pytest.mark.parametrize("n, expected", [
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (8, 40320),
    #(25, 15511210043330985984000000),
    #(30, 265252859812191058636308480000000),
    #(40, 815915283247897734345611269596115894272000000000),
    #(50, 30414093201713378043612608166064768844377641568960512000000000000),
])
def test_calc_factorial(n, expected, benchmark):
    res = benchmark.pedantic(calc_factorial, args=(n,))
    assert expected == res
