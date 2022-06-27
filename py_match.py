"""
File:    py_match.py
Author:  Chance Bell
Date:    4/22/2022
Section: 30-LEC (1648)
E-mail:  cbell3@umbc.edu
Description:
  When ran, py_match.py receives user inputs to assign variables for the size of our grid, the seed, and to read a file.
  Next, the function play_game is defined in which it uses our initial inputs to create our grid and a 2-D list of
  randomly indexed letters. Each element is returned and passed into our other function called run_game. run_game uses
  a series of if statements, for loops, and while loops to simulate a users turn to guess. 2-D lists are
  manipulated to put correctly answered inputs into our printed grid. Deep copies of our 2-D lists are used as temporary
  list so that we may either fall back on our original list, or assign our original list to our temporary list. If all
  the letters are revealed on the grid, the user wins.
"""

import random

def play_game(row, col, seed, letters):
    random.seed(int(seed))
    ans_list = list()
    board = list()

    for i in range(int(row)): # creates two 2d arrays to display our grid and for our letters
        board.append([])
        ans_list.append([])
        for j in range(int(col)):
            board[i].append('.')
            ans_list[i].append(random.choice(letters))

    return ans_list, board, letters, row, col
    # returned arguments that are used in the function run_game as passed


def run_game(passed):
    board = passed[1]
    check_list = list()
    pos_list = list()

    while board != passed[0]: # checks if the 2d array == the random array of letters
        for i in board:
            print('  '.join(i))
        pos_y, pos_x = input('Enter a position to guess: ').split(' ')
        if 0 < int(pos_y) <= int(passed[3]) and 0 < int(pos_x) <= int(passed[4]):
            pos = passed[0][int(pos_y)-1][int(pos_x)-1] # simplified variable for ease of access

        if pos_y + pos_x not in pos_list:
            pos_list.append(pos_y + pos_x)
        count = 0 # setting count for when we find a letter that has more than one on the board

        if 0 < int(pos_y) <= int(passed[3]) and 0 < int(pos_x) <= int(passed[4]):
            for i in passed[0]: # gets which letter has more than one on the board and sets its count
                for j in i:
                    if j == pos:
                        count += 1

            if count == 1 and pos not in check_list: # if there is only one of that letter on the board
                print(f'You have found all of the {pos}')
                board[int(pos_y) - 1][int(pos_x) - 1] = pos
                check_list.append(pos)
                count = 0
            elif count > 1 and pos not in check_list: # has more than one on the board
                temp_list = [row[:] for row in board] # creates a deep copy of our board and positions
                temp_pos = [row[:] for row in pos_list]

                while count != 1:
                    temp_list[int(pos_y) - 1][int(pos_x) - 1] = pos
                    broke = False
                    count -= 1
                    for i in temp_list:
                        print('  '.join(i))
                    pos_y, pos_x = input(f'Enter position to guess that matches {pos}, there are '
                          f'{count} remaining: ').split(' ')
                    if passed[0][int(pos_y)-1][int(pos_x)-1] == pos:
                        # checks to see if our newly inputted positions are the same letter as our initial one
                        temp_list[int(pos_y) - 1][int(pos_x) - 1] = pos
                    if pos_y + pos_x in temp_pos and passed[0][int(pos_y)-1][int(pos_x)-1] == pos:
                        print('You have already guessed that value, please enter a new position')
                        count += 1 # returns a round to the user by adding a count if they guessed the same pos
                    else:
                        temp_pos.append(pos_y + pos_x)
                    if passed[0][int(pos_y)-1][int(pos_x)-1] != pos:
                        # if our new position is not the same letter as our initial position
                        print('Try again!')
                        temp_pos = pos_list
                        broke = True
                        count = 1
                if count == 1 and broke != True: # once count becomes 1, you have found all the corresponding letters
                    print(f'You have found all of the {pos}')
                    board = temp_list
                    check_list.append(pos)
                    count = 0

            elif count >= 1 and pos in check_list:
                print(f'You have already found all of the {pos}')
        else:
            print('Please enter a position in range') # if our inputted positions are out of range

    for i in board:
        print('  '.join(i))
    print(f'Congratulations, you win!')


if __name__ == '__main__':
    row, col, seed = input('Enter Row, Col, Seed: ').split(',')

    file_name = input("Enter a file to read from: ")
    with open(file_name, 'r') as my_file: # opens and reads the inputted file name
        read_text = my_file.read()
        letters = list(read_text.split())

    play_game(row, col, seed, letters)
    run_game(play_game(row, col, seed, letters))
