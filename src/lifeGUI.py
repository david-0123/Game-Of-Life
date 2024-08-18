import random as rnd
import time
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

# Generates the initial game state with 'dead' cells weighted more, i.e. 'dead' cells should be expected more often
def random_state(width, height):
    board = [[rnd.choices(population=[0,1], weights=[0.85,0.15], k=1)[0] for x in range(width)] for y in range(height)]
    return board

# Generates a board with only dead cells
def dead_state(width, height):
    board = [[0 for x in range(width)] for y in range(height)]
    return board

# Loads the initial state of the board from a config file made of 1s and 0s
def load_state(file):
    with open(file, 'r') as f:
        loaded = f.readlines()

    initBoard = [[int(num) for num in line if num != '\n'] for line in loaded]

    # If config file is empty load a dead state board
    if len(initBoard) == 0:
        initBoard = dead_state(1,1)

    return initBoard

# Calculates the state of the board after the next round
def next_state(board):
    height = len(board)
    width = len(board[0])

    next_board = dead_state(width, height)

    # Loops through each board cell
    for x in range(height):
        for y in range(width):
            current = board[x][y]
            currentAlive = current != 0

            liveNeighbours = 0

            # Loops each cell's neighbours
            for a in range(x-1, x+2):
                for b in range(y-1, y+2):
                    try:
                        if board[a][b] == 1 and a >= 0 and b >= 0 and (a,b) != (x,y):
                            liveNeighbours += 1
                    except IndexError:
                        pass

            # Applies rules that determine which cells become/stay alive
            if currentAlive and 2 <= liveNeighbours <= 3:
                next_board[x][y] = 1
            elif not currentAlive and liveNeighbours == 3:
                next_board[x][y] = 1

    return next_board

def render(board, stdscr, boxHeight, boxWidth, gridHeight, gridWidth):
    stdscr.erase()
    stdscr.border()
    for i in range(gridHeight):
        for j in range(gridWidth):
            for y in range(boxHeight-1):
                for x in range(boxWidth-1):
                    if board[i][j] == 1:
                        stdscr.addch(y+i+1, x+j+1, ' ', curses.A_REVERSE)
                    else:
                        stdscr.addch(y+i+1, x+j+1, ' ')
    stdscr.move(0,0)
    stdscr.refresh()

def menu(stdscr):
    box_height, box_width = (2,3)
    stdscr.nodelay(True)

    mode = ''

    while mode not in ['load','go']:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(curses.LINES//2-8, curses.COLS//2-25, "Welcome to Conway's Game of Life!")
        stdscr.addstr(curses.LINES//2-6, curses.COLS//2-25, "Controls: 'q' to end simulation")
        stdscr.addstr(curses.LINES//2-4, curses.COLS//2-25, "Type 'load' to run a custom board, 'go' to run a random soup, or 'quit' to exit the game")

        modeWin = curses.newwin(1, 20, curses.LINES//2, curses.COLS//2-5)
        modeBox = Textbox(modeWin)
        stdscr.refresh()
        modeBox.edit()
        mode = modeBox.gather().lower().strip().replace('\n', '')

        if mode == 'load':
            stdscr.addstr(curses.LINES//2+3, curses.COLS//2-25, "Type the name of the file (with extension) to load")
            fileWin = curses.newwin(1, 20, curses.LINES//2+5, curses.COLS//2-5)
            fileBox = Textbox(fileWin)
            stdscr.refresh()
            fileBox.edit()
            fileName = fileBox.gather().strip().replace('\n', '')
            try:
                initBoard = load_state(fileName)
                gridWidth = len(initBoard[0])
                gridHeight = len(initBoard)
            except FileNotFoundError:
                print("File not found")
                quit()

        elif mode == 'go':
            gridWidth = curses.COLS - box_width
            gridHeight = curses.LINES - box_height
            initBoard = random_state(gridWidth, gridHeight)

        elif mode == 'quit':
            quit()

        else:
            stdscr.addstr(curses.LINES//2+10, curses.COLS//2, "Invalid command")
            stdscr.refresh()
            time.sleep(1)

    play(stdscr, initBoard, box_height, box_width, gridHeight, gridWidth)

def play(stdscr, board, box_height, box_width, gridHeight, gridWidth):
    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key == chr(ord("q")):
            menu(stdscr)
            break

        render(board, stdscr, box_height, box_width, gridHeight, gridWidth)
        board = next_state(board)
        time.sleep(0.1)

        '''
        TODO:
        - allow user to terminate round/whole program with keyboard
        - scalability formatting
        - allow user to change config settings? (play/pause/speed/starting live cells etc)
        '''

def main(stdscr):
    menu(stdscr)

wrapper(main)