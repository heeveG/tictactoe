from board import Board, OutOfRangeError, NotEmptyError

board = Board()
while board.has_winner() == 0:
    try:
        x, y = input("Input your move:\n").split()
        cell = (int(x), int(y))
    except ValueError:
        print("Enter two integer values please.")
        continue

    try:
        board.make_move(cell)
    except OutOfRangeError:
        print('Input out of range. Please reenter.')
        continue
    except NotEmptyError:
        print('The cell is not empty. Please reenter.')
        continue

    if board.has_winner() == -1:
        print('You won!')
        break
    elif board.has_winner() == 2:
        print("Draw.")
        break

    board = board.tree()
    print(board)
else:
    if board.has_winner() == 1:
        print('You lost!')
    elif board.has_winner() == 2:
        print("Draw.")
