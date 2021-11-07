"""
   :synopsis: Asyncio example from the book
"""

from typing import Generator


def range_generator(n) -> Generator:
    i = 0
    while i < n:
        print(f"Generating value {i}")
        yield i
        i += 1

