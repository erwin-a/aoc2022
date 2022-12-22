from utils import Pos, Board, Range, Pos3, bounding_cube, fill_outside


def test_Pos():
    p = Pos(0, 0)
    t = Pos(2, 0)
    assert list(p.draw(t)) == [Pos(0, 0), Pos(1, 0), Pos(2, 0)]

    # manhattan distance
    assert (p - t).md() == 2

    # 1 md circle, where does it overlap y=0
    assert p.overlap_yline(1, y=0) == Range(-1, +1)
    assert p.overlap_yline(1, y=1) == Range(0, 0)
    assert p.overlap_yline(1, y=-1) == Range(0, 0)
    assert p.overlap_yline(1, y=2) == None


def test_Range():
    assert Range(0, 1) & Range(1, 2)
    assert not (Range(0, 1) & Range(2, 3))


def test_Board():
    b = Board()
    b.draw(Pos(1, 0), Pos(4, 0))
    b.draw(Pos(0, 2), Pos(0, 3))
    b.fill_empty()
    print()
    b.dump()

    assert sum(1 for _ in b.find_all('#')) == 6

    b = Board.from_str(["###", ".#"])
    assert b.miny == b.minx == 0
    assert b.maxx == 2
    assert sum(1 for _ in b.find_all('#')) == 4
    assert b[1, 0] == '#'

    b2 = b.translate(dx=1, dy=0)
    assert b2.minx == 1
    assert b2.maxx == 3
    assert b.collides(b2)
    b3 = b.translate(dx=5, dy=0)
    assert not b.collides(b3)


def test_Pos3():
    s = {Pos3(1, 1, 1)}
    top, bot = bounding_cube(s)
    assert top == (0, 0, 0)
    assert bot == (2, 2, 2)

    s = {Pos3(1, 1, 1), Pos3(2, 2, 1)}
    top, bot = bounding_cube(s)
    assert top == (0, 0, 0)
    assert bot == (3, 3, 2)

    assert len(set(Pos3.plane(Pos3(0, 0, 0), Pos3(2, 2, 2), z=3))) == 9
    assert len(set(Pos3.plane(Pos3(0, 0, 0), Pos3(2, 2, 2), y=3))) == 9
    assert len(set(Pos3.plane(Pos3(0, 0, 0), Pos3(2, 2, 2), x=3))) == 9

    assert len(fill_outside({Pos3(1,1,1)})) == 26
    assert len(fill_outside({Pos3(1,1,1)}, gap=2)) == 5 * 5 + 5 * 5 + 3 * 5 + 3 * 5 + 3 * 3 + 3 * 3
