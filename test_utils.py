from utils import Pos, Board


def test_Pos():
    p = Pos(0,0)
    t = Pos(2,0)
    assert list(p.draw(t)) == [Pos(0,0), Pos(1,0), Pos(2,0)]

def test_Board():
    b = Board()
    b.draw(Pos(1,0), Pos(4,0))
    b.draw(Pos(0,2), Pos(0,3))
    b.fill_empty()
    print()
    b.dump()

    assert sum(1 for _ in b.find_all('#')) == 6
