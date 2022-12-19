import itertools

from utils import lines, Board, Pos


def read(n):
    return ['<>'.index(x)*2-1 for x in next(lines(n))]

shapes = [
    [{0,1,2,3}],

    [{1}, {0,1,2}, {1}],

    [{2}, {2}, {0,1,23}],

    [{0}, {0}, {0}, {0}],

    [{0,1}, {0,1}]
]


W = 7
def main():
    next_jet = itertools.cycle(read("17a")).__next__
    b = Board()

    top = B

    for x in range(5):
        pass


if __name__ == '__main__':
    main()
