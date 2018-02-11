import time
import os
from threading import Thread
from pynput.keyboard import Key, Listener


class Game:
    def __init__(self):
        # constants
        self.data = {'fps': 5, 'width': 50, 'height': 29}

        # region keyboard listener
        def on_press(key):
            if key.name in ['up', 'down', 'left', 'right']:
                self.delete_character()
                self.char.move(key.name, self.data['height'], self.data['width'])
                self.move_character()

        def on_release(key):
            if key == Key.esc:
                self.running = False
                return False

        self.keyboard = Listener(on_press=on_press, on_release=on_release)
        self.keyboard.start()
        # endregion

        # create the board
        self.board = create_board(self.data['height'], self.data['width'])

        # region create the character
        class Character:
            def __init__(self, i, j, value):
                self.i = i
                self.j = j
                self.value = value

            def move(self, direction, max_height, max_width):
                # check out of bounds error
                if (self.i == 0 and direction == 'up') or (self.i == max_height-1 and direction == 'down'):
                    return
                if (self.j == 1 and direction == 'left') or (self.j == max_width-2 and direction == 'right'):
                    return

                # change the position according to direction
                if direction == 'up':
                    self.i -= 1
                elif direction == 'down':
                    self.i += 1
                elif direction == 'left':
                    self.j -= 1
                elif direction == 'right':
                    self.j += 1

        self.char = Character(25, 25, '+')
        self.move_character()
        # endregion

        # thread to run the mainloop
        self.t = Thread(target=self.mainloop)
        self.running = False

    def run(self):
        self.running = True
        self.t.start()
        self.t.join()

    def delete_character(self):
        self.board[self.char.i][self.char.j] = ' '

    def move_character(self):
            self.board[self.char.i][self.char.j] = self.char.value

    def mainloop(self):
        t1 = time.time()
        t2 = t1
        interval = 1/self.data['fps']
        while True:
            if not self.running:
                return
            while t2 - t1 <= interval:
                t2 = time.time()
            else:
                t1 = t2
                self.render()

    def render(self):
        cls()
        print_board(self.board)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(board):
    for row in board:
        for j in range(len(row)):
            print(row[j], end='')
        print()


def create_board(height, width):
    board = [[' '] * (width - 2) for _ in range(height)]
    for i in range(height):
        board[i] = ['|'] + board[i] + ['|']
    return board


