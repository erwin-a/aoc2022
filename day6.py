###
### Day 6
###
def read():
    return open("inputs/6.txt").read()


def main(size):
    s = read()
    for i in range(len(s)):
        if len(set(s[i:i+size])) == size:
            print(i + size)
            break


if __name__ == '__main__':
    main(4)
    main(14)
