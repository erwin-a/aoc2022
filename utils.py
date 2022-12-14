import itertools
import operator
from collections import namedtuple
from functools import reduce


def replace_nth(t: tuple, n: int, val):
    "Replace nth in the tuple with val"
    t = list(t)
    t[n] = val
    return tuple(t)


def join(seq):
    l = []
    for x in seq:
        l.extend(x)
    return l

def product(s):
    return reduce(operator.mul, s)

class Pos(namedtuple('Pos', 'x y')):
    x: int
    y: int
    def __add__(self, o: 'Pos'):
        return Pos(self.x + o.x, self.y + o.y)

    def __sub__(self, o: 'Pos'):
        return Pos(self.x - o.x, self.y - o.y)

    def absmax(self):
        return max(abs(self.x), abs(self.y))

    def __repr__(self):
        return "{%3d,%3d}" % (self.x, self.y)

    def sign(self):
        return Pos(sign(self.x), sign(self.y))

    def __bool__(self):
        return bool(self.x or self.y)

    def draw(self, target):
        cur = self
        while 1:
            yield cur
            if not (diff := target - cur):
                break
            cur += diff.sign()

    @classmethod
    def from_str(cls, s):
        return cls(*map(int, s.split(',')))



def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return +1
    else:
        return 0

from heapq import heappush, heappop, heapify


TOMBSTONE = -1, -1

class PriorityQueue:
    "priority queue using heapq module; existing items can be modified"
    def __init__(self, items=None):
        self.pq = []
        self.index = {}  # item -> [value, item] for updates to existing items
        if items:
            for (k, v) in items:
                self.index[k] = (t := [v, k])
                self.pq.append(t)
            heapify(self.pq)

    def __getitem__(self, k):
        return self.index[k][0]

    def __setitem__(self, item, value):
        # allow update of existing item: do not remove it but mark its value as "dead"
        # and create new item
        try:
            self.index[item][1] = TOMBSTONE
        except KeyError:
            pass
        self.index[item] = (t := [value, item])
        heappush(self.pq, t)

    def pop(self):
        "pop smallest item"
        while 1:
            t = heappop(self.pq)
            if t[1] != TOMBSTONE:   # removed items marked as such, skip them
                return t[1]

identity = lambda x:x

def lines(f):
    for line in open("inputs/%s.txt" % f):
        yield line.rstrip()
def tokens(f):
    for line in lines(f):
        yield line.split()


diff = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Board:
    def __init__(self):
        self.d = {} # x,y -> height; y grows
        self.maxx = self.maxy = -1

    def __setitem__(self, k, v):
        self.d[k] = v
        self.maxx = max(self.maxx, k[0])
        self.maxy = max(self.maxy, k[1])

    def find_first(self, wanted):
        return next(self.find_all(wanted))
    def find_all(self, wanted):
        for k,v in self.d.items():
            if v == wanted:
                yield k

    def itery(self):
        for y in range(self.maxy+1): yield y

    def iterx(self):
        for x in range(self.maxx+1): yield x

    def row(self, y):
        return [self[x, y] for x in self.iterx()]
    def col(self, x):
        return [self[x, y] for y in self.itery()]

    def draw(self, start: Pos, end: Pos, char='#'):
        diff = start-end
        assert diff.x == 0 or diff.y == 0
        for x in start.draw(end):
            self[x] = char


    def iterrc(self):
        for y in self.itery():
            for x in self.iterx():
                yield x, y, self[x,y], self.row(y), self.col(x)


    def neighbours(self, xy):
        for d in diff:
            try:
                k = xy[0] + d[0], xy[1] + d[1]
                yield k, self[k]
            except KeyError:
                pass

    def __getitem__(self, k):
        return self.d[k]
    def __contains__(self, item):
        return item in self.d

    def positions(self):
        return self.d.keys()

    @classmethod
    def from_rows(cls, seq, fun=identity):
        self = cls()
        for y, line in enumerate(seq):
            for x, item in enumerate(line):
                self[x,y] = fun(item)
        return self

    def iter_rows(self):
        for y in range(self.maxy+1):
            yield y, [self.d[x,y] for x in range(self.maxx + 1)]

    def fill_empty(self, char='.'):
        for x in self.iterx():
            for y in self.iterx():
                try:
                    self[x,y]
                except KeyError:
                    self[x,y] = char

    def dump(self):
        for _, row in self.iter_rows():
            print (''.join(row))



def shorted_distances(positions, start, neighbours):
    unvisited = set(positions)
    distance = PriorityQueue((x, 2 ** 32) for x in unvisited)
    distance[start] = 0

    while unvisited:
        cur = distance.pop()
        for there, cost in neighbours(cur):
            if there in unvisited:
                distance[there] = min(distance[there], distance[cur] + cost)
        unvisited.discard(cur)
    return distance


class Range(namedtuple('Range', 'start end')):
    @classmethod
    def from_str(cls, s, delim='-'):
        return cls(*map(int, s.split(delim)))

    def __and__(self, o: 'Range'):
        return self.start <= o.end and o.start <= self.end

    def within(self, o: 'Range'):
        return self.start >= o.start and self.end <= o.end
