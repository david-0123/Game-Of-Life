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
    for y in range(height):
        for x in range(width):
            current = board[y][x]
            currentAlive = current != 0

            liveNeighbours = 0

            # Loops each cell's neighbours
            for a in range(y-1, y+2):
                for b in range(x-1, x+2):
                    try:
                        if board[a][b] == 1 and a >= 0 and b >= 0 and (a,b) != (y,x):
                            liveNeighbours += 1
                    except IndexError:
                        pass

            # Applies rules that determine which cells become/stay alive
            if currentAlive and 2 <= liveNeighbours <= 3:
                next_board[y][x] = 1
            elif not currentAlive and liveNeighbours == 3:
                next_board[y][x] = 1

    return next_board

# Updates the terminal to show the current board state
def render(board, stdscr, gridHeight, gridWidth):
    stdscr.erase()
    stdscr.border()
    for i in range(gridHeight): # For each row
        for j in range(gridWidth): # For each column
            if board[i][j] == 1:
                #Uses whitespace with reversed bg/fg, so it appears as a white box
                stdscr.addch(i+1, j+1, ' ', curses.A_REVERSE)
            else:
                stdscr.addch(i+1, j+1, ' ')
    stdscr.move(curses.LINES-1, curses.COLS-1) #Moves the cursor to the bottom right, so it's out of the way
    stdscr.refresh()

# Displays flashing text on the screen
def flashText(stdscr, colourPair, y, x, text):
    curses.curs_set(0)
    stdscr.attron(colourPair)
    for i in range(2):
        stdscr.addstr(y, x, text)
        stdscr.refresh()
        time.sleep(1)

        stdscr.addstr(y, x, ' ' * len(text))
        stdscr.refresh()
        time.sleep(0.5)
    stdscr.attroff(colourPair)

def checkRectangularBoard(board):
    width = len(board[0])

    for row in board:
        if len(row) != width:
            return False

    return True

# Handles the display and logic of the menu screen
def menu(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    redOnBlack = curses.color_pair(1)
    stdscr.nodelay(True)

    TITLE_Y_COORD = curses.LINES//3
    TITLE_X_COORD = (curses.COLS*2)//5

    exitLoop = False

    # Loops until a valid command is entered
    while not exitLoop:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(TITLE_Y_COORD, TITLE_X_COORD+6, "Welcome to Conway's Game of Life!")
        stdscr.addstr(TITLE_Y_COORD+2, TITLE_X_COORD-3, "Press any key to end the simulation after it starts")
        stdscr.addstr(TITLE_Y_COORD+4, TITLE_X_COORD-24, "Type 'load' to run a custom pattern, 'go' to run a random pattern, or 'quit' to exit the game")

        modeWin = curses.newwin(1, 5, TITLE_Y_COORD+6, curses.COLS//2-2)
        modeBox = Textbox(modeWin)
        stdscr.hline(TITLE_Y_COORD+7, curses.COLS//2-3, curses.ACS_HLINE, 6)

        stdscr.refresh()
        curses.curs_set(1)
        modeBox.edit()
        stdscr.refresh()

        mode = modeBox.gather().lower().strip().replace('\n', '')

        if mode == 'load':
            stdscr.addstr(TITLE_Y_COORD+10, TITLE_X_COORD-17, "Config files must be text files containing a rectangular grid of only 1s and 0s")
            stdscr.addstr(TITLE_Y_COORD+12, TITLE_X_COORD+1, "Type the file name (with extension) to load")
            fileWin = curses.newwin(1, 20, TITLE_Y_COORD+14, curses.COLS//2-3)
            fileBox = Textbox(fileWin)

            stdscr.refresh()
            fileBox.edit()
            fileName = fileBox.gather().strip().replace('\n', '')

            try:
                initBoard = load_state(fileName)
                gridWidth = len(initBoard[0])
                gridHeight = len(initBoard)
                exitLoop = checkRectangularBoard(initBoard)
            except FileNotFoundError:
                flashText(stdscr, redOnBlack, TITLE_Y_COORD+20, TITLE_X_COORD+15, "File Not Found!")
            except ValueError:
                flashText(stdscr, redOnBlack, TITLE_Y_COORD+20, TITLE_X_COORD+13, "Invalid Config File")

        elif mode == 'go':
            gridWidth = curses.COLS - 2
            gridHeight = curses.LINES - 2
            initBoard = random_state(gridWidth, gridHeight)
            exitLoop = True

        elif mode == 'quit':
            quit()

        else:
            flashText(stdscr, redOnBlack, TITLE_Y_COORD+20, TITLE_X_COORD+15, "Invalid Command")

    play(stdscr, initBoard, gridHeight, gridWidth)

# Handles the infinite simulation
def play(stdscr, board, gridHeight, gridWidth):
    playing = True

    while playing:
        try:
            key = stdscr.getch()
        except:
            key = None

        # Any key press terminates the game
        if key != -1:
            playing = False
            menu(stdscr)

        render(board, stdscr, gridHeight, gridWidth)
        board = next_state(board)
        time.sleep(0.1)

def main(stdscr):
    menu(stdscr)

wrapper(main)

'''
TODO:
- allow user to change settings? (play/pause/speed)
- allow user to manually click and place starting live cells before playing
'''