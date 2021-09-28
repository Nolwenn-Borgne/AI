"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Initialize count of X and O
    count_x = 0
    count_o = 0

    # Loops on the board to count X and O
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1

    # Returns player who has the next turn on a board
    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Initialize the set of possible actions
    possible_actions = set()

    # Loops on the board to check the EMPTY case
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    # Returns all possible actions available on the board
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # if action is not a valid action for the board, we raise an exception
    if action not in actions(board):
        raise Exception("This action is not valid")

    # makes a copy of the board before doing the action
    new_board = copy.deepcopy(board)

    # changes the board
    new_board[action[0]][action[1]] = player(board)

    # returns the board that results from making move
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # defines the players list
    players = [X, O]

    # checks the rows
    for row in range(3):
        for player_sign in players:
            if board[row][0] == board[row][1] == board[row][2] == player_sign:
                return player_sign

    # checks the columns
    for col in range(3):
        for player_sign in players:
            if board[0][col] == board[1][col] == board[2][col] == player_sign:
                return player_sign

    # checks the diagonals
    for player_sign in players:
        if board[0][0] == board[1][1] == board[2][2] == player_sign:
            return player_sign
        if board[0][2] == board[1][1] == board[2][0] == player_sign:
            return player_sign

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if someone has won (winner function returns X or O)
    if winner(board) in (X, O):
        return True

    # or all the cells have been filled(actions set is empty)
    elif actions(board) == set():
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None

    if terminal(board):
        return None
    elif player(board) == X:
        best_value = -math.inf

        # for each possible action, we calculate the value of min_value and we keep the action with the highest value
        for action in actions(board):
            action_value = min_value(result(board, action))

            if action_value > best_value:
                best_value = action_value
                best_action = action

                # if the value is 1, we have found a winning action and we don't have to go further
                if best_value == 1:
                    break
    else:
        best_value = math.inf

        # for each possible action, we calculate the value of max_value and we keep the action with the lowest value
        for action in actions(board):
            action_value = max_value(result(board, action))

            if action_value < best_value:
                best_value = action_value
                best_action = action

                # if the value is -1, we have found a winning action and we don't have to go further
                if best_value == -1:
                    break

    return best_action


def min_value(board):
    """
    Returns the lowest value
    """

    v = math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def max_value(board):
    """
    Returns the highest value
    """

    v = -math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v
