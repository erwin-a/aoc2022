## Day 5
##
STACKS = 9

def read():
    fh = open("inputs/5.txt")
    positions = [(x, x*4+1) for x in range(STACKS)]
    stacks = [[] for _ in range(STACKS)]

    for line in fh:
        if not (line := line.rstrip("\r\n")):
            break
        for stack, position in positions:
            if (ch := line[position]).isupper():
                stacks[stack].insert(0, ch)

    commands = []
    for line in fh:
        l = line.split()
        commands.append((int(l[1]), int(l[3])-1, int(l[5])-1)) # move 2 from 4 to 9
    return stacks, commands

def main(stride):
    stacks, commands = read()
    for n, source, target in commands:
        stacks[source], crates = stacks[source][:-n], stacks[source][-n:][::stride]
        stacks[target].extend(crates)

    print (''.join(x[-1] for x in stacks))

if __name__ == '__main__':
    main(-1)
    main(+1)


