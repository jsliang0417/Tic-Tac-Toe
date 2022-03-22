from math import inf
from random import choice
import argparse
import time


#parse argument
parser = argparse.ArgumentParser()
parser.add_argument("--method", help="minimax or alpha-beta pruning")
args = parser.parse_args()



human = -1
bot = 1
game_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

human_choice = 'X'
bot_choice = 'O'

moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2],
    4: [1, 0], 5: [1, 1], 6: [1, 2],
    7: [2, 0], 8: [2, 1], 9: [2, 2]
}


def analyze(game_board):
    point = 0
    if victory(game_board, human):
        point -= 1
    elif victory(game_board, bot):
        point += 1
    else:
        point = 0
    return point



def valid_movement(x, y):
    if [x, y] in empty_cells(game_board):
        return True
    else:
        return False
        

def update_move(x, y, turn):
    if valid_movement(x, y):
        game_board[x][y] = turn
        return True
    else:
        return False
    
    
def minimax(game_board, depth, turn):
    if turn == bot:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]
    
    if depth == 0 or game_over(game_board):
        point = analyze(game_board)
        return [-1, -1, point]
    
    for i in empty_cells(game_board):
        x = i[0]
        y = i[1]
        game_board[x][y] = turn
        point = minimax(game_board, depth-1, -turn)
        game_board[x][y] = 0
        point[0] = x
        point[1] = y
        if turn == bot:
            if point[2] > best[2]:
                best = point
        else:
            if point[2] < best[2]:
                best = point
    return best


def alphaBetaPruning(game_board, depth, turn, alpha, beta):
    if turn == bot:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]
    
    if depth == 0 or game_over(game_board):
        point = analyze(game_board)
        return [-1, -1, point]
    
    for i in empty_cells(game_board):
        x = i[0]
        y = i[1]
        game_board[x][y] = turn
        x, y= alphaBetaPruning(game_board, depth-1, -turn, alpha, beta)
        
        if x > best:
            best = x
        if best > alpha:
            alpha = best
        if alpha > beta:
            print("prune")
            break
        
    return best




def victory(game_board, turn):
    victory_case = [
        [game_board[0][0], game_board[0][1], game_board[0][2]],
        [game_board[1][0], game_board[1][1], game_board[1][2]],
        [game_board[2][0], game_board[2][1], game_board[2][2]],
        [game_board[0][0], game_board[1][0], game_board[2][0]],
        [game_board[0][1], game_board[1][1], game_board[2][1]],
        [game_board[0][2], game_board[1][2], game_board[2][2]],
        [game_board[0][0], game_board[1][1], game_board[2][2]],
        [game_board[2][0], game_board[1][1], game_board[0][2]],
    ]
    
    if [turn, turn, turn] in victory_case:
        return True
    else:
        return False


def empty_cells(game_board):
    cells = []
    for i, row in enumerate(game_board):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([i, y])
    return cells



def game_over(game_board):
    return victory(game_board, human) or victory(game_board, bot)


def human_turn(b_choice, h_choice):
    depth = len(empty_cells(game_board))
    if depth == 0 or game_over(game_board):
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2]
    }
    
    print("Human's turn: {0}".format(h_choice))
    print_board(game_board, b_choice, h_choice)
    
    while move < 1 or move > 9:
        try:
            move = int(input("Please enter 1~9: "))
            location = moves[move]
            available_move = update_move(location[0], location[1], human)
            
            if not available_move:
                print("Illegal Movement")
                move = -1
        except:
            print("Exit...")
            exit()



def bot_turn(b_choice, h_choice):
    depth = len(empty_cells(game_board))
    if depth == 0 or game_over(game_board):
        return
    
    print("Bot's turn: {0}".format(b_choice))
    print_board(game_board, b_choice, h_choice)
    
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game_board, depth, bot)
        x = move[0]
        y = move[1]
    
    update_move(x, y, bot)


def print_board(game_board, b_choice, h_choice):
    pairs = {
        -1: h_choice,
        1: b_choice,
        0: ' '
    }
    
    cut_line = "_________"
    
    print("\n" + cut_line)
    
    for i in game_board:
        for j in i:
            s = pairs[j]
            print("{0} |".format(s), end='')
        print("\n" + cut_line)




def main():
    
    
    
    if args.method == "minimax":
        print("Using Minimax")
        while len(empty_cells(game_board)) > 0 and not game_over(game_board):
            human_turn(bot_choice, human_choice)
            bot_turn(bot_choice, human_choice)
        
        if victory(game_board, human):
            print("Human's turn: {0}".format(human_choice))
            print_board(game_board, bot_choice, human_choice)
            print("Human Win")
        elif victory(game_board, bot):
            print("Bot's turn: {0}".format(bot_choice))
            print_board(game_board, bot_choice, human_choice)
            print("Bot Win")
        else:
            print_board(game_board, bot_choice, human_choice)
            print("Tie")
    
    
    if args.method == "ab-pruning":
        print("Using Alpha-Beta Pruning")





if __name__ == '__main__':
    main()
    