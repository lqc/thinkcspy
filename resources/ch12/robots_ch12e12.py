#
# robots.py
#
from gasp import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_WIDTH = SCREEN_WIDTH/10 - 1
GRID_HEIGHT = SCREEN_HEIGHT/10 - 1


def place_player():
    x = random.randint(0, GRID_WIDTH)
    y = random.randint(0, GRID_HEIGHT)
    return {'shape': Circle((10*x+5, 10*y+5), 5, filled=True), 'x': x, 'y': y}


def place_robot():
    x = random.randint(0, GRID_WIDTH)
    y = random.randint(0, GRID_HEIGHT)
    return {'shape': Box((10*x, 10*y), 10, 10), 'x': x, 'y': y}


def place_robots(numbots):
    robots = []
    for i in range(numbots):
        robots.append(place_robot())
    return robots


def move_player(player):
    update_when('key_pressed')
    if key_pressed('escape'):
        return True
    elif key_pressed('4'):
        if player['x'] > 0: player['x'] -= 1
    elif key_pressed('7'):
        if player['x'] > 0: player['x'] -= 1
        if player['y'] < GRID_HEIGHT: player['y'] += 1
    elif key_pressed('8'):
        if player['y'] < GRID_HEIGHT: player['y'] += 1
    elif key_pressed('9'):
        if player['x'] < GRID_WIDTH: player['x'] += 1
        if player['y'] < GRID_HEIGHT: player['y'] += 1
    elif key_pressed('6'):
        if player['x'] < GRID_WIDTH: player['x'] += 1
    elif key_pressed('3'):
        if player['x'] < GRID_WIDTH: player['x'] += 1
        if player['y'] > 0: player['y'] -= 1
    elif key_pressed('2'):
        if player['y'] > 0: player['y'] -= 1
    elif key_pressed('1'):
        if player['x'] > 0: player['x'] -= 1
        if player['y'] > 0: player['y'] -= 1
    elif key_pressed('0'):
        player['x'] = random.randint(0, GRID_WIDTH)
        player['y'] = random.randint(0, GRID_HEIGHT)
    else:
        return False

    move_to(player['shape'], (10*player['x']+5, 10*player['y']+5))

    return False


def collided(thing1, thing2):
    return thing1['x'] == thing2['x'] and thing1['y'] == thing2['y']


def check_collisions(robots, junk, player):
    for thing in robots + junk:
        if collided(thing, player):
            return True
    return False


def move_robot(robot, player):
    if robot['x'] < player['x']: robot['x'] += 1
    elif robot['x'] > player['x']: robot['x'] -= 1

    if robot['y'] < player['y']: robot['y'] += 1
    elif robot['y'] > player['y']: robot['y'] -= 1

    move_to(robot['shape'], (10*robot['x'], 10*robot['y']))


def move_robots(robots, player):
    for robot in robots:
        move_robot(robot, player)


def play_game():
    begin_graphics(SCREEN_WIDTH, SCREEN_HEIGHT)
    player = place_player()
    robots = place_robots(2)
    junk = [{'shape': Box((320, 240), 10, 10, filled=True), 'x': 32, 'y': 24}]
    defeated = False

    while not defeated:
        quit = move_player(player)
        if quit:
            break
        move_robots(robots, player)
        defeated = check_collisions(robots, junk, player)

    if defeated:
        remove_from_screen(player['shape'])
        for thing in robots + junk:
            remove_from_screen(thing['shape'])
        Text("They got you!", (240, 240), size=32)
        sleep(3)

    end_graphics()


if __name__ == '__main__':
    play_game()
