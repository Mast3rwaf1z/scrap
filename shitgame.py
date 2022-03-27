from getpass import getpass
from time import sleep, time
from scrap_engine import Object, Map, screen_height, screen_width, Text, Box
from pynput import keyboard
from threading import Thread
from os import system, name
from sys import exit

# initialization
l_combination = {"left", "space"}
r_combination = {"right", "space"}
u_combination = {"up", "space"}
d_combination = {"down", "space"}
coords = [int(screen_width/2), int(screen_height/2)]
current_keys = set()
projectiles:list[tuple[Text, str]] = list()
map:Map
player:Box
running = True

# specific function definitions
def projectile_builder(direction:str) -> tuple[Text, str]:
    global map
    match direction:
        case "up":
            projectile = Object(char="^")
            projectile.add(map, coords[0] + int(len(player.obs)/2), coords[1]-1)
        case "left":
            projectile = Object(char="<")
            projectile.add(map, coords[0]-1, coords[1])
        case "down":
            projectile = Object(char="V")
            projectile.add(map, coords[0] + int(len(player.obs)/2), coords[1]+1)
        case "right":
            projectile = Object(char=">")
            projectile.add(map, coords[0] + len(player.obs), coords[1])
    return projectile, direction

def projectile_move(projectile:tuple[Object, str]):
    global map
    alive = True
    while alive:
        match projectile[1]:
            case "up":
                projectile[0].set(projectile[0].x, projectile[0].y-1)
            case "left":
                projectile[0].set(projectile[0].x-1, projectile[0].y)
            case "down":
                projectile[0].set(projectile[0].x, projectile[0].y+1)
            case "right":
                projectile[0].set(projectile[0].x+1, projectile[0].y)
        if projectile[0].y == 1 or projectile[0].x == 1 or projectile[0].y == screen_height-3 or projectile[0].x == screen_width-2:
            projectile[0].remove()
            alive = False
        map.show()

def keep_alive():
    global running
    getpass(prompt="")
    running = False
    exit()

# listener functions
def on_press(key:keyboard.KeyCode | keyboard.Key):
    global projectiles, current_keys, coords
    try:
        k = key.char
    except:
        k = key.name
    if not k in current_keys and (k in u_combination or l_combination or d_combination or r_combination):
        current_keys.add(k)
    match k:
        case "a":
            if not coords[0] <= 1:
                coords[0] -= 1
        case "d":
            if not coords[0] >= screen_width-(len(player.obs)+1):
                coords[0] += 1
        case "w":
            if not coords[1] <= 1:
                coords[1] -= 1
        case "s":
            if not coords[1] >= screen_height-3:
                coords[1] += 1
    if current_keys == u_combination and player.y > 1:
        projectiles.append(projectile_builder("up"))
    elif current_keys == l_combination and player.x > 1:
        projectiles.append(projectile_builder("left"))
    elif current_keys == d_combination and player.y < screen_height-3:
        projectiles.append(projectile_builder("down"))
    elif current_keys == r_combination and player.x < screen_width - (len(player.obs) + 1):
        projectiles.append(projectile_builder("right"))
    player.set(coords[0], coords[1])
    map.show()

def on_release(key:keyboard.Key | keyboard.KeyCode):
    global current_keys
    try:
        k = key.char
    except:
        k = key.name
    if k in current_keys:
        current_keys.remove(k)

if __name__ == "__main__":
    #start menu
    character = "( ͡° ͜ʖ ͡°)"
    _in = "( ͡° ͜ʖ ͡°)"
    while character == _in:
        system("cls" if name == "nt" else "clear")
        print("______________________________SHITGAME!______________________________")
        print("Controls:")
        print("w:                   Move up")
        print("a:                   Move left")
        print("s:                   Move down")
        print("d:                   Move right")
        print("Space + arrow key:   Shoot in a direction")
        print("Enter:               Exit the game")
        _in = input(f'type your character (leave blank to start, current={character}): ') 
        if _in == "":
            break
        character = _in

    #init
    player = Box(1,8)
    [player.add_ob(Object(character[i]), i,0) for i in range(len(character))]
    map = Map(background=" ")
    map.show(init=True)
    player.add(map, coords[0], coords[1])
    game_title = " SHITGAME! "
    box = Box(screen_height, screen_width)
    [box.add_ob(Object(char="#"), i, screen_height-2) for i in range(screen_width)]
    [box.add_ob(Object(char="#"), screen_width-1, i) for i in range(screen_height-1)]
    box.add_ob(Text(text=game_title),int(screen_width/2-len(game_title)/2), 0)
    [box.add_ob(Object(char="#"), i, 0) for i in range(screen_width)]
    [box.add_ob(Object(char="#"), 0, i) for i in range(1, screen_height-1)]
    box.add(map, 0, 0)
    projectiles.append(projectile_builder("up"))

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    Thread(target=keep_alive).start()
    while running: 
        if len(projectiles) > 0:
            for projectile in projectiles:
                projectiles.remove(projectile) 
                Thread(target=projectile_move,args=(projectile,)).start()
        map.show()
        sleep(.1)
