from collections import defaultdict, Counter
from random import choice
from string import ascii_uppercase
from patricia import trie
import timeit
from functools import lru_cache


def counter_defaultdict(items: list):
    dd = defaultdict(int)
    for item in items:
        dd[item] += 1
    print(dd)


def counter_strike(items: list):
    dd = Counter(items)
    print(dd)


def process_counters():
    items: list = [1, 2, 3, 4]
    counter_defaultdict(items)
    counter_strike(items)


def search_word(word: str, docs: list):
    matches = [doc for doc in docs if word in doc]
    print(matches)


def inverted_index(word: str, docs: list):
    """
    Improved version of search_word method thanks to preprocessing
    """
    index: dict = {}
    for i, doc in enumerate(docs):
        for ww in doc.split():
            if ww not in index:
                index[ww] = {i}
            else:
                index[ww].add(i)
    results = index[word]
    print(index["cat"].intersection(results))
    result_doc = [docs[i] for i in results]
    print(result_doc)


def process_words():
    docs = [
        "the cat is under the table",
        "the dog is under the table",
        "cats and dogs smell roses",
        "Carla eats an apple",
    ]
    search_word("table", docs)
    inverted_index("table", docs)


def random_string(lentgh: int) -> str:
    return "".join(choice(ascii_uppercase) for i in range(lentgh))


def process_strings():
    strings = [random_string(32) for i in range(10000)]
    matches = [s for s in strings if s.startswith("AA")]


def process_strings_optimized():
    strings = [random_string(32) for i in range(10000)]
    strings_dict = {s: 0 for s in strings}
    strings_trie = trie(**strings_dict)
    matches = list(strings_trie.iter("AA"))


def timeit_process_strings():
    # 18.6643249
    print(timeit.timeit(stmt=process_strings, number=100))
    # 26.371805733
    # it's not optimized because of unpacking
    print(timeit.timeit(stmt=process_strings_optimized, number=100))


def fibonacci(n):
    if n < 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_cache():
    fibonacci_memoized = lru_cache(maxsize=None)(fibonacci)
    print(timeit.timeit(stmt=fibonacci_memoized(20), number=100))
    print(timeit.timeit(stmt=fibonacci(20), number=100))


if __name__ == "__main__":
    # process_counters()
    # process_words()
    # timeit_process_strings()
    fibonacci_cache()
