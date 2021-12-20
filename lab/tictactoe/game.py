import os


class Game():
    def __init__(self, state=None):
        # state of game board
        self.state = state if state is not None else [0] * 9

        # the number of moves
        self.moves = 9 - self.state.count(0)

        # current player, -1 for "X" player, 1 for "O" player
        self.player = ((self.moves % 2) - 1) & 1

    def getExecutableIndices(self):
        ret = []
        for i in range(len(self.state)):
            if self.state[i] == 0:
                ret.append(i)
        return ret

    def move(self, index: int) -> bool:
        """
        Move for specified player
        :param index: position of grid
        :return:
        """
        if not 0 <= index <= 8 or self.state[index] != 0:
            print('Illegal move!')
            return False
        self.state[index] = self.player
        self.player *= -1  # exchange player
        self.moves += 1
        return True

    def print(self):
        """
        Print the game board on console
        """

        def get_filler(index):
            return {0: ' ', -1: 'X', 1: 'O'}[self.state[index]]

        for i in range(3):
            print('-------')
            print('|' + get_filler(i * 3) + '|' + get_filler(i * 3 + 1) + '|' + get_filler(i * 3 + 2) + '|')
        print('-------')

    def sumOf(self, *indices):
        ret = 0
        for index in indices:
            ret += self.state[index]
        return ret

    def isWin(self) -> bool:
        """
        Judge whether current player wins.
        """
        cond = (-self.player) * 3

        # check three rows
        for i in range(3):
            if self.sumOf(i * 3, i * 3 + 1, i * 3 + 2) == cond:
                return True

        # check three columns
        for i in range(3):
            if self.sumOf(i, i + 3, i + 6) == cond:
                return True

        # check diagonals
        if self.sumOf(0, 4, 8) == cond or self.sumOf(2, 4, 6) == cond:
            return True

        # otherwise
        return False

    def start(self):
        """
        Start a new game on console.
        """
        os.system("clear")  # clear console
        self.print()  # empty board
        while True:
            prompt = ('X' if self.player == -1 else 'O') + ' player move: '
            choose = input(prompt)
            if not choose.isdigit():
                break
            if self.move(int(choose)):
                os.system("clear")  # clear console
                self.print()
            if self.moves == 9 and not self.isWin():
                print("Draw.")
                break
            if self.isWin():
                print(('X' if -self.player == -1 else 'O') + ' player wins!')
                break
        print("Game over.")
