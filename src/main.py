import random as rnd

def random_state(width, height):
    board = [[rnd.choice((0,1)) for x in range(width)] for y in range(height)]

    return board

print(random_state(5, 5))