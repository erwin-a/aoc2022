from utils import lines, Pos3, fill_outside, bounding_cube


def read(n):
    for x in lines(n):
        yield Pos3.from_str(x)


def main():
    cubes = set(read("18"))
    shared = set()
    for c in cubes:
        for n in c.neighbours():
            if n in cubes:
                shared.add((c, n))
    print (6*len(cubes) - len(shared))
    return

def ff(start, water, cubes, sides):
    stack = [start]
    seen = set(stack)

    while stack:
        pos = stack.pop(-1) # constant time
        for d in pos.neighbours():
            if d in water: continue # already wet
            if d in cubes:
                sides.add((pos, d))
                continue
            if d not in seen:
                stack.append(d)
                seen.add(d)

def main2():
    cubes = set(read("18"))
    # leave 1 empty space between the cubes and the water
    bot, _ = bounding_cube(cubes, S=1)
    water = fill_outside(cubes, S=2)

    # starting at the bottom, flood fill the area outside of the cubes
    # count every time try to enter a cube
    sides = set()
    ff(bot, water, cubes, sides)
    print (len(sides))


if __name__ == '__main__':
    main()
    main2()

