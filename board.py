import copy
import random
from btree import BTree
from btnode import BTNode


class OutOfRangeError(BaseException):
    pass


class NotEmptyError(BaseException):
    pass


def generate_winning_combinations():
    """
    Generates all possible winning combinations
    <Code is taken from Oles Dobosevych example!>
    :return: list
    """
    combinations = []
    for i in range(3):
        combination1 = []
        combination2 = []
        for j in range(3):
            combination1.append((i, j))
            combination2.append((j, i))
        combinations.append(combination1)
        combinations.append(combination2)

    combinations.append([(0, 0), (1, 1), (2, 2)])
    combinations.append([(0, 2), (1, 1), (2, 0)])
    return combinations


# Some methods are implemented using Oles Dobosevych example
class Board:
    """
    Board class
    """
    NOUGHT = 1
    CROSS = -1
    EMPTY = 0

    NOUGHT_WINNER = 1
    CROSS_WINNER = -1
    DRAW = 2
    NOT_FINISHED = 0

    WINNING_COMBINATIONS = generate_winning_combinations()

    def __init__(self):
        """
        Initiates board object
        """
        self.cells = [[0] * 3 for _ in range(3)]
        self.last_move = Board.NOUGHT
        self.number_of_moves = 0

    def make_move(self, cell):
        """
        Sets a marker on a given cell. Raises error if impossible to set a marker on given position.
        :param cell: tuple
        """
        try:
            if self.cells[cell[0]][cell[1]] != 0:
                raise NotEmptyError()
        except IndexError:
            raise OutOfRangeError()
        self.last_move = -self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def has_winner(self):
        """
        Checks if the game has ended and return the winner
        :return: int
        """
        for combination in self.WINNING_COMBINATIONS:
            lst = []
            for cell in combination:
                lst.append(self.cells[cell[0]][cell[1]])
            if max(lst) == min(lst) and max(lst) != Board.EMPTY:
                return max(lst)
        if self.number_of_moves == 9:
            return Board.DRAW

        return Board.NOT_FINISHED

    def make_random_move(self):
        """
        Makes random move
        """
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == Board.EMPTY:
                    possible_moves.append((i, j))
        cell = random.choice(possible_moves)
        self.last_move = -self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def tree(self):
        """
        Chooses one of two random moves using tree
        """
        tree = BTree()
        board1 = copy.deepcopy(self)
        board2 = copy.deepcopy(self)

        board1.make_random_move()
        board2.make_random_move()
        tree.set_left(BTNode(board1))
        tree.set_right(BTNode(board2))

        def recurse(board):
            if board.item.has_winner() == 0:
                l1 = copy.deepcopy(board.item)
                l2 = copy.deepcopy(board.item)
                l1.make_random_move()
                l2.make_random_move()
                board.left = BTNode(l1)
                board.right = BTNode(l2)
                return recurse(board.left) + recurse(board.right)
            has_winner = board.item.has_winner()
            if has_winner:
                winner_scores = {Board.NOUGHT_WINNER: 1, Board.CROSS_WINNER: -1, Board.DRAW: 0}
                return winner_scores[has_winner]

        r1 = recurse(tree.root.left)
        r2 = recurse(tree.root.right)
        if r1 > r2:
            return board1
        else:
            return board2

    def __str__(self):
        """
        String representation of board
        """
        symbols = {0: " ", 1: "O", -1: "X"}
        return "\n".join(["_|_".join(map(lambda x: symbols[x], row)) for row in self.cells])
