# TBD wrong on real data set now

import dataclasses
import math
from itertools import islice
from typing import Any

from utils import lines


def read(f):
    for x in lines(f):
        yield int(x)


def main():
    # items can have dupes!
    items = list(enumerate(read("20")))
    N = len(items)
    l = ll(items)
    for x in items:
        #print (x[0], ["%s:%s"%  (y.item) for y in l])
        #print (x[0], [y.item[1] for y in l])

        _, offset = x
        #print(f"move, {x} offset {offset}")
        # find node that will be after this item
        if offset == 0:
            continue
        elif offset < 0:
            forward = offset % N
        elif offset > 0:
            forward = (offset + 1) % N
        else:
            assert 0

        node = l.find_item(x)
        new_next = l.advance(node, forward)
        #print(f"advance {node} to before {new_next} ({forward})")
        if node is not new_next:
            l.remove(node)
            l.insert_before(node, new_next)

    print ([y.item[1] for y in l])
    zero = find_item(l, 0)

    il = []
    for v in [1000, 2000, 3000]:
        n = l.advance(zero, v)
        il.append(n.item[1])
    print (il, sum(il))




@dataclasses.dataclass
class Node:
    prev: 'Node'
    item: int
    next: 'Node'
    def __repr__(self):
        return str(self.item)

class ll:
    items: list[Node]
    N: int

    def __init__(self, items: list[Any]):
        self.N = N = len(items)

        self.items = i = [Node(None, 0, None) for _ in range(N)]
        for xi, x in enumerate(items):
            i[xi].prev = i[(xi-1) % N]
            i[xi].next = i[(xi+1) % N]
            i[xi].item = x

    def remove(self, x: Node):
        x.prev.next, x.next.prev = x.next, x.prev
        x.next = x.prev = None

    def insert_before(self, n:Node, b: Node):
        assert n is not b
        assert n.prev is None and n.next is None
        n.prev, b.prev.next = b.prev, n
        n.next, b.prev = b, n

    def find_item(self, item):
        for node in self:
            if node.item == item:
                return node
        assert 0

    def advance(self, item, n):
        n = n % self.N
        return next(islice(self.iter_from(item), n, n+1))

    def iter_from(self, start: Node):
        cur = start
        while 1:
            yield cur
            cur = cur.next
            if cur is start:
                break


    def __iter__(self):
        # arbitrary order, but once
        yield from self.iter_from(self.items[0])

def find_item(l: ll, val) -> Node:
    x: Node
    for x in l:
        if x.item[1] == val:
            return x
    assert 0

if __name__ == '__main__':
    main()
