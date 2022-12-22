from utils import lines, Pos3, fill_outside, bounding_cube


def read(n) -> set[Pos3]:
    return {Pos3.from_str(x) for x in lines(n)}


def main():
    cubes = read("18")
    shared = set()
    for c in cubes:
        for n in c.neighbours():
            if n in cubes:
                shared.add((c, n))
    assert 4444 == 6 * len(cubes) - len(shared)


def ff(start, water, cubes):
    "non-recursive 3D flood fill"
    sides = set()
    stack = [start]
    seen = set(stack)

    while stack:
        pos = stack.pop(-1)  # constant time for last element
        for d in pos.neighbours():
            if d in cubes:
                sides.add((pos, d))
            elif d not in water and d not in seen:
                stack.append(d)
                seen.add(d)
    return sides


def main2():
    cubes = read("18")
    # leave 1 empty space between the cubes and the water
    bot, _ = bounding_cube(cubes, gap=1)
    water = fill_outside(cubes, gap=2)

    # starting at the bottom, flood fill the area outside of the cubes
    # count every time try to enter a cube
    sides = ff(bot, water, cubes)
    assert 2530 == len(sides)


if __name__ == '__main__':
    main()
    main2()
