import random
import copy
import sys
import math
import numpy as np
import time

nodes_expanded = 0
sys.setrecursionlimit(40000)
print('ENTER THE BOARD SIZE n: ')
grid_size = int(input())
depth_limit = 4
player = 'computerMove'
comp_move_number = 0
possible_number = [2, 2, 2, 2, 4]
grid = np.zeros((grid_size, grid_size), dtype=int)

gameRunning = True


def find_best_move(board):
    move = 0
    value = -math.inf

    board1 = copy.deepcopy(board)
    if is_left_possible(board1):
        board1 = move_left(board1)
        # print('after move left')
        result = pruning(board1, -math.inf, math.inf, False, 0)
        # print(result, 'best_move_left')
        if result >= value:
            move = 1
            value = result

    board1 = copy.deepcopy(board)
    if is_right_possible(board1):
        board1 = move_right(board1)
        result = pruning(board1, -math.inf, math.inf, False, 0)

        if result >= value:
            move = 2
            value = result

    board1 = copy.deepcopy(board)
    if is_up_possible(board1):
        board1 = move_up(board1)
        result = pruning(board1, -math.inf, math.inf, False, 0)

        if result >= value:
            move = 3
            value = result

    board1 = copy.deepcopy(board)
    if is_down_possible(board1):
        board1 = move_down(board1)
        result = pruning(board1, -math.inf, math.inf, False, 0)
        
        if result >= value:
            move = 4

    return move


def computer_generates_move(board, comp_move):
    empty_list = []
    empty_list.clear()
    board_size = len(board)

    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                empty_list.append((i, j))

    if len(empty_list) > 0:
        r, c = random.choice(empty_list)
        num1 = random.choice(possible_number)
        board[r][c] = num1
        empty_list.pop(empty_list.index((r, c)))

    if comp_move == 1:
        r, c = random.choice(empty_list)
        num1 = random.choice(possible_number)
        board[r][c] = num1

    return board


def is_game_over(board):
    board_size = len(board)

    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                return False

    for i in range(board_size):
        for j in range(board_size):
            if i != 0 and board[i][j] == board[i - 1][j]:
                return False

            if i != board_size - 1 and board[i][j] == board[i + 1][j]:
                return False

            if j != 0 and board[i][j] == board[i][j - 1]:
                return False

            if j != board_size - 1 and board[i][j] == board[i][j + 1]:
                return False

    return True


def move_left(board):
    board_size = len(board)
    board1 = copy.deepcopy(board)
    for row in range(board_size):
        new_row = np.zeros(board_size, dtype=int)
        col2 = 0
        previous = None
        for col1 in range(board_size):
            if board1[row][col1] != 0:  # number different from zero
                if previous is None:
                    previous = board1[row][col1]
                else:
                    if previous == board1[row][col1]:
                        new_row[col2] = 2 * board1[row][col1]
                        col2 += 1
                        previous = None
                    else:
                        new_row[col2] = previous
                        col2 += 1
                        previous = board1[row][col1]
        if previous is not None:
            new_row[col2] = previous
        for col in range(board_size):
            board1[row][col] = new_row[col]

    return board1


def move_right(board):
    board_size = len(board)
    board1 = copy.deepcopy(board)
    board1 = move_left(board1)
    for row in range(board_size):
        count = board_size - 1
        while count != 0:
            for col1 in range(board_size - 1, 0, -1):
                col2 = col1 - 1
                if board1[row][col1] == 0:
                    board1[row][col1] = board1[row][col2]
                    board1[row][col2] = 0
            count = count - 1

    return board1


def move_up(board):
    board1 = copy.deepcopy(board)
    board1 = np.rot90(board1, 1)
    board1 = move_left(board1)
    board1 = np.rot90(board1, 3)

    return board1


def move_down(board):
    board1 = copy.deepcopy(board)
    board1 = np.rot90(board1, 3)
    board1 = move_left(board1)
    board1 = np.rot90(board1, 1)

    return board1


def is_left_possible(board):
    board1 = copy.deepcopy(board)
    board1 = move_left(board1)
    if np.array_equal(board, board1):
        return False
    return True


def is_right_possible(board):
    board1 = copy.deepcopy(board)
    board1 = move_right(board1)
    if np.array_equal(board, board1):
        return False
    return True


def is_up_possible(board):
    board1 = copy.deepcopy(board)
    board1 = move_up(board1)
    if np.array_equal(board, board1):
        return False
    return True


def is_down_possible(board):
    board1 = copy.deepcopy(board)
    board1 = move_down(board1)
    if np.array_equal(board, board1):
        return False
    return True


def max_board(board):
    board_size = len(board)
    heuristics = np.zeros((4, board_size, board_size), dtype=int)
    count = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                count = count + 1
    fill_val = 0
    for index in range(4):
        for row in range(board_size):
            if index == 0 or index == 1:
                fill_val = board_size - row - 1
            for col in range(board_size):
                if index == 0:
                    heuristics[index][row][col] = fill_val - col
                elif index == 1:
                    heuristics[index][row][col] = -(fill_val - col)
                elif index == 2:
                    heuristics[index][row][col] = row - col
                elif index == 3:
                    heuristics[index][row][col] = -(row - col)

    maxb = -math.inf
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] > maxb:
                maxb = board[row][col]
    maxb1 = math.log2(maxb)
    cscore = clustering_score(board, board_size)
    values = np.zeros(4)
    for index in range(4):
        for row in range(board_size):
            for col in range(board_size):
                values[index] += heuristics[index][row][col] * board[row][col]
            values[index] += (count+maxb1)
            values[index] -= cscore

    return max(values)


def clustering_score(board, board_size):
    cs = 0
    neighbors = [-1, 0, -1]
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                continue
            number_of_neighbors = 0
            sums = 0
            for k in neighbors:
                x = i+k
                if x < 0 or x >= board_size:
                    continue
                for l in neighbors:
                    y = j+l
                    if y < 0 or y >= board_size:
                        continue
                    if board[i][j] > 0:
                        number_of_neighbors = number_of_neighbors+1
                        sums = sums + abs(board[i][j]-board[x][y])

            cs = sums/number_of_neighbors
    return cs


def pruning(board, a, b, chance, depth):
    global nodes_expanded
    board_size = len(board)
    board1 = copy.deepcopy(board)
    if is_game_over(board):
        return max_board(board)

    if depth >= depth_limit:
        return max_board(board)

    if chance:
        score = -math.inf
        board = move_left(board)
        nodes_expanded = nodes_expanded+1

        score = max(score, pruning(board, a, b, not chance, depth+1))
        if score >= b:
            return score
        a = max(score, a)
        board = copy.deepcopy(board1)
        board = move_right(board)
        nodes_expanded = nodes_expanded + 1

        score = max(score, pruning(board, a, b, not chance, depth)+1)
        if score > b:
            return score
        a = max(score, a)
        board = copy.deepcopy(board1)
        board = move_up(board)
        nodes_expanded = nodes_expanded + 1

        score = max(score, pruning(board, a, b, not chance, depth+1))
        if score > b:
            return score
        a = max(score, a)
        board = copy.deepcopy(board1)
        board = move_down(board)
        nodes_expanded = nodes_expanded + 1

        score = max(score, pruning(board, a, b, not chance, depth+1))
        if score > b:
            return score
        a = max(score, a)
        board = copy.deepcopy(board1)

        return score

    else:
        score = math.inf

        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == 0:

                    board[i][j] = 4
                    nodes_expanded = nodes_expanded + 1
                    score = min(score, pruning(board, a, b, not chance, depth+1))
                    if score <= a:
                        board[i][j] = 0
                        return score
                    b = min(score, b)
                    board[i][j] = 2
                    nodes_expanded = nodes_expanded + 1
                    score = min(score, pruning(board, a, b, not chance, depth+1))
                    if score <= a:
                        board[i][j] = 0
                        return score
                    b = min(score, b)
                    board[i][j] = 0
        return score


def display_board(board):
    board_size = len(board)
    for i in range(board_size):
        print('\n')
        for j in range(board_size):
            if board[i][j] == 0:
                print('   ', end=' | ')
            else:
                print('  ' + str(board[i][j]), end=' | ')
        print('\n')
        if i != board_size - 1:
            for k in range(board_size * 3):
                print('-', end='-')


start_time = time.time()
while gameRunning:

    if player == "computerMove":
        print("Computer's Turn!")

        comp_move_number = comp_move_number + 1

        grid = computer_generates_move(grid, comp_move_number)
        display_board(grid)
        score = is_game_over(grid)
        if is_game_over(grid):
            gameRunning = False
            break
        player = "AIMove"

    if player == "AIMove":
        print("\nAI's Turn!")

        m = find_best_move(grid)
        if m == 1:
            grid = move_left(grid)
        elif m == 2:
            grid = move_right(grid)
        elif m == 3:
            grid = move_up(grid)
        elif m == 4:
            grid = move_down(grid)
        display_board(grid)
        player = "computerMove"

end_time = time.time()
print("No of nodes expanded", nodes_expanded)
print("Time taken", (end_time - start_time))
