##
##
from utils import Range


def read():
    for line in open("inputs/4.txt"):
        yield [Range.from_str(x) for x in line.strip().split(',')]


def main():
    a: Range
    b: Range
    assert 459 == sum(1 for a, b in read() if a.within(b) or b.within(a))
    assert 459 == sum(1 for a,b  in read() if a.within(b) or b.within(a))
    assert 779 == sum(1 for a, b in read() if a & b)


if __name__ == '__main__':
    main()
