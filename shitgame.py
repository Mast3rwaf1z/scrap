from getpass import getpass
from random import randint
from time import sleep, time
from scrap_engine import Object, Map, screen_height, screen_width, Text, Box
from pynput import keyboard
from threading import Thread
from os import system, name
from sys import exit

from modules.client import Client
from modules.host import Host

# initialization
ur_combination = {"up", "right", "space"}
u_combination = {"up", "space"}
ul_combination = {"up", "left", "space"}
l_combination = {"left", "space"}
dl_combination = {"down", "left", "space"}
d_combination = {"down", "space"}
dr_combination = {"down", "right", "space"}
r_combination = {"right", "space"}
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
            projectile = Object(char="▲")
            projectile.add(map, player.x + int(len(player.obs)/2), player.y-1)
        case "upright":
            projectile = Object(char="◥")
            projectile.add(map, player.x+ len(player.obs), player.y-1)
        case "left":
            projectile = Object(char="◀")
            projectile.add(map, player.x-1, player.y)
        case "upleft":
            projectile = Object(char="◤")
            projectile.add(map, player.x-1, player.y-1)
        case "down":
            projectile = Object(char="▼")
            projectile.add(map, player.x + int(len(player.obs)/2), player.y+1)
        case "downleft":
            projectile = Object(char="◣")
            projectile.add(map, player.x-1, player.y+1)
        case "right":
            projectile = Object(char="▶")
            projectile.add(map, player.x + len(player.obs), player.y)
        case "downright":
            projectile = Object(char="◢")
            projectile.add(map, player.x + len(player.obs), player.y+1)
    return projectile, direction

def projectile_move(projectile:tuple[Object, str]):
    global map
    alive = True
    while alive:
        match projectile[1]:
            case "up":
                projectile[0].set(projectile[0].x, projectile[0].y-1)
            case "upright":
                projectile[0].set(projectile[0].x+1, projectile[0].y-1)
            case "left":
                projectile[0].set(projectile[0].x-1, projectile[0].y)
            case "upleft":
                projectile[0].set(projectile[0].x-1, projectile[0].y-1)
            case "down":
                projectile[0].set(projectile[0].x, projectile[0].y+1)
            case "downleft":
                projectile[0].set(projectile[0].x-1, projectile[0].y+1)
            case "right":
                projectile[0].set(projectile[0].x+1, projectile[0].y)
            case "downright":
                projectile[0].set(projectile[0].x+1, projectile[0].y+1)
        if projectile[0].y == 1 or projectile[0].x == 1 or projectile[0].y == screen_height-3 or projectile[0].x == screen_width-2:
            projectile[0].remove()
            alive = False
        sleep(.05)
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
            if not player.x <= 1:
                tmp = player.x - 1
                player.set(tmp, player.y)
        case "d":
            if not player.x >= screen_width-(len(player.obs)+1):
                tmp = player.x + 1
                player.set(tmp, player.y)
        case "w":
            if not player.y <= 1:
                tmp = player.y - 1
                player.set(player.x, tmp)
        case "s":
            if not player.y >= screen_height-3:
                tmp = player.y + 1
                player.set(player.x, tmp)
    if current_keys == u_combination and player.y > 1:
        projectiles.append(projectile_builder("up"))
    elif current_keys == ur_combination and player.y > 1 and player.x < screen_width - (len(player.obs) + 1):
        projectiles.append(projectile_builder("upright"))
    elif current_keys == l_combination and player.x > 1:
        projectiles.append(projectile_builder("left"))
    elif current_keys == ul_combination and player.y > 1 and player.x > 1:
        projectiles.append(projectile_builder("upleft"))
    elif current_keys == d_combination and player.y < screen_height-3:
        projectiles.append(projectile_builder("down"))
    elif current_keys == dl_combination and player.y < screen_height-3 and player.x > 1:
        projectiles.append(projectile_builder("downleft"))
    elif current_keys == r_combination and player.x < screen_width - (len(player.obs) + 1):
        projectiles.append(projectile_builder("right"))
    elif current_keys == dr_combination and player.y < screen_height-3 and player.x < screen_width - (len(player.obs) + 1):
        projectiles.append(projectile_builder("downright"))
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
    start_msg = "______________________________SHITGAME!______________________________\n"+\
    "Controls:\n"+\
    "w:                   Move up\n"+\
    "a:                   Move left\n"+\
    "s:                   Move down\n"+\
    "d:                   Move right\n"+\
    "Space + arrow key:   Shoot in a direction\n"+\
    "Enter:               Exit the game\n\n"+\
    "Script states:\n"+\
    "1:                   host TBD\n"+\
    "2:                   client TBD\n"+\
    "3:                   single player\n"
    states = ["host", "client", "single player"]
    script_state = "single player"
    character = "( ͡° ͜ʖ ͡°)"
    while True:
        system("cls" if name == "nt" else "clear")
        print(start_msg)
        _in = input(f'choose the state of this script (leave blank to confirm, current={script_state}): ')
        if _in == "":
            break
        try:
            state = states[int(_in)-1]
        except:
            print("input is invalid")
            sleep(1)
        script_state = state
    while True:
        system("cls" if name == "nt" else "clear")
        print(start_msg)
        char = input(f'type your character (leave blank to confirm, current={character}): ') 
        if char == "":
            break
        character = char

    # gamestates:
    match script_state:
        case "host":
            host = Host()
        case "client":
            client = Client()
        case "single player":
            pass

    #init
    player = Box(1,8)
    [player.add_ob(Object(character[i]), i,0) for i in range(len(character))]
    map = Map(background=" ")
    map.show(init=True)
    player.add(map, randint(1, screen_width-(len(player.obs)-1)), randint(1,screen_height-3))
    game_title = " SHITGAME! "
    box = Box(screen_height, screen_width)
    [box.add_ob(Object(char="#"), i, screen_height-2) for i in range(screen_width)]
    [box.add_ob(Object(char="#"), screen_width-1, i) for i in range(screen_height-1)]
    box.add_ob(Text(text=game_title),int(screen_width/2-len(game_title)/2), 0)
    [box.add_ob(Object(char="#"), i, 0) for i in range(screen_width)]
    [box.add_ob(Object(char="#"), 0, i) for i in range(1, screen_height-1)]
    box.add(map, 0, 0)

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    Thread(target=keep_alive).start()

    if script_state == "client":
        client.player = player
        send_thread = Thread(target=client.sendpos)
        send_thread.start()


    while running: 
        if len(projectiles) > 0:
            for projectile in projectiles:
                projectiles.remove(projectile) 
                Thread(target=projectile_move,args=(projectile,)).start()
        map.show()
        sleep(.1)
