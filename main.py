import time
import os
from threading import Thread


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    g = Game()
    g.run()


def print_board(board):
    for row in board:
        try:
            for j in range(len(row)):
                print(row[j], end='')
        except IndexError:
            pass
        print()


def create_board(height, width):
    board = [[' '] * (width - 2) for _ in range(height)]
    for i in range(height):
        board[i] = ['|'] + board[i] + ['|']
    return board


class Game:
    def __init__(self):
        # constants
        self.data = {'fps': 10, 'width': 40, 'height': 29, 'track_length': 60}

        # create the board
        self.board = create_board(self.data['track_length'], self.data['width'])
        # some noticeable values
        self.board[0][5] = 1
        self.board[self.data['height']-1][6] = 9
        self.board[3][5] = 7
        self.board[self.data['height'] + 10][6] = 2

        # thread to run the mainloop
        self.t = Thread(target=self.mainloop)

    def run(self):
        self.t.start()
        input("Press enter to close...")

    def mainloop(self):
        t1 = time.time()
        t2 = t1
        interval = 1/self.data['fps']
        start_row = 0
        while True:
            while t2 - t1 <= interval:
                t2 = time.time()
            else:
                t1 = t2
                self.render(start_row)
                start_row += 1
                if start_row > self.data['track_length']:
                    return

    def render(self, start_row):
        cls()
        print_board(self.board[start_row:start_row+self.data['height']])

if __name__ == "__main__":
    main()
