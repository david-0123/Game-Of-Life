import random as rnd

# Generates the initial game state with 'dead' cells weighted more, i.e. 'dead' cells should be expected more often
def random_state(width, height):
    board = [[rnd.choices(population=[' ', chr(0x25A0)], weights=[0.8,0.2], k=1)[0] for x in range(width)] for y in range(height)]
    return board

# Displays the current game state on the terminal with the correct format
def render(board):
    print(" "+chr(0x035F)*10)
    for i in range(len(board)):
        print(chr(0x2502), end="")
        for j in range(len(board[i])):
            print(board[i][j], end="")
        print(chr(0x2502))
    print(" "+chr(0x035E)*10)

render(random_state(10, 5))