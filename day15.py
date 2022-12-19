from cpmpy import Model, intvar  # https://cpmpy.readthedocs.io/en/latest/index.html
from utils import lines, Pos, Range
import re

# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
rx = re.compile('.* x=([-\d]+).*y=([-\d]+).*x=([-\d]+).*y=([-\d]+)')

FILENAME, TARGET_Y, MAX_COORD = 15, 2_000_000, 4_000_000


# Test setup
# fn, TY, max_coord = "15a", 10, 20

def read():
    for x in lines(FILENAME):
        x, y, x2, y2 = map(int, rx.search(x).groups())
        yield Pos(x, y), Pos(x2, y2)


# https://en.wikipedia.org/wiki/Sweep_line_algorithm
def swl(l: list[Range]):
    t = 0
    prev = None
    for r in sorted(l):
        if prev is None or not r & prev:
            t += r.length
        elif r.within(prev):
            continue
        else:
            overlap = prev.end - r.start + 1
            t += r.length - overlap
        prev = r
    return t


def main():
    ranges = []
    excluded = set()

    for s, b in read():
        d = (s - b).md()
        if (o := s.overlap_yline(d, y=TARGET_Y)) is not None:
            ranges.append(o)
        if b.y == TARGET_Y:
            excluded.add(b)  # beacons can overlap!

    # spots that contain a beacon cannot NOT contain a beacon!
    print(swl(ranges) - len(excluded))


def main2():
    m = Model()
    X, Y = intvar(lb=0, ub=MAX_COORD, shape=2)
    for s, b in read():
        d = (s - b).md()
        m += (abs(X - s.x) + abs(Y - s.y)) > d

    assert m.solve()
    print(X.value(), Y.value(), X.value() * 4000000 + Y.value())


if __name__ == '__main__':
    main()
    main2()
