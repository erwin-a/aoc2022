from utils import Board, shorted_distances


def main():
    board = Board.from_rows(
        reversed([line.strip()
                  for line in open("inputs/12.txt")]))

    board[end := board.find_first('S')] = 'a'
    board[start := board.find_first('E')] = 'z'

    def neighbours(cur):    # paths we can safely walk down from
        for xy, h in board.neighbours(cur):
            if ord(h) >= ord(board[cur]) - 1:
                yield xy, 1

    distances = shorted_distances(positions=board.positions(),
                                  start=start, neighbours=neighbours)

    print(distances[end])
    print(min(distances[x] for x in board.find_all('a')))


if __name__ == '__main__':
    main()
