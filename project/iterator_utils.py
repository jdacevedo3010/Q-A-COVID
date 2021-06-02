from typing import TypeVar, Iterator
from functools import reduce

A = TypeVar("A")

def take (n: int, xs: Iterator[A]) -> Iterator[A]:
    cnt = 0
    for x in xs:
        if cnt == n:
            break
        yield x
        cnt += 1

def size (xs: Iterator[A]) -> int:
    return reduce(lambda acc, _: acc + 1, xs, 0)