import random as rnd

# Generates the initial game state with 'dead' cells weighted more, i.e. 'dead' cells should be expected more often
def random_state(width, height):
    board = [[rnd.choices(population=[0,1], weights=[0.8,0.2], k=1)[0] for x in range(width)] for y in range(height)]
    return board

def dead_state(width, height):
    board = [[0 for x in range(width)] for y in range(height)]
    return board

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

# Displays the current game state on the terminal with the correct format
#  ͟͟͟͟͟͟͟͟͟͟
# │■   ■     │
# │   ■    ■ │
# │   ■      │
# │     ■ ■ ■│
# │         ■│
#  ͞͞͞͞͞͞͞͞͞͞
def render(board):
    print(" "+chr(0x035F)*10)
    for i in range(len(board)):
        print(chr(0x2502), end="")
        for j in range(len(board[i])):
            if board[i][j] == 0:
                symbol = ' '
            else:
                symbol = chr(0x25A0)
            print(symbol, end="")
        print(chr(0x2502))
    print(" "+chr(0x035E)*10)

render(random_state(10, 5))