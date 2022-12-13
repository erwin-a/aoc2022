import math
from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest, chain


def read():
    for chunk in open("inputs/13.txt").read().split("\n\n"):
        left, right = map(literal_eval, chunk.strip().split("\n"))
        yield left, right


class Yes(Exception):
    pass


class No(Exception):
    pass


def compare_inner(l, r):
    match l, r:
        case int(l), int(r):
            if l < r:
                raise Yes
            elif l > r:
                raise No

        case list(l), list(r):
            for lx, rx in zip_longest(l, r):  # shortest sequence will see None padding
                if lx is None:
                    raise Yes
                elif rx is None:
                    raise No
                compare_inner(lx, rx)

        case int(l), list(r):
            compare_inner([l], r)
        case list(l), int(r):
            compare_inner(l, [r])
        case _:
            assert 0, (l, r)


def compare(l, r):
    try:
        compare_inner(l, r)
    except Yes:
        return -1
    except No:
        return +1
    else:
        assert 0


def main():
    print(sum(
        xi + 1
        for xi, (left, right) in enumerate(read())
        if compare(left, right) < 0
    ))

    dividers = ([[2]], [[6]])
    flat = sorted(chain(*read(), dividers), key=cmp_to_key(compare))  # no more cmp for sort in py3

    print(math.prod(
        xi + 1
        for xi, x in enumerate(flat)
        if x in dividers
    ))


if __name__ == '__main__':
    main()
