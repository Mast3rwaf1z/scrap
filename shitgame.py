from getpass import getpass
from scrap_engine import Object, Map, screen_height, screen_width, Text
from pynput import keyboard
from threading import Thread

l_combination = {"left", "space"}
r_combination = {"right", "space"}
u_combination = {"up", "space"}
d_combination = {"down", "space"}
coords = [int(screen_width/2), int(screen_height/2)]
current_key = set()
projectiles:list[Thread] = list()

map = Map(background=" ")
o = Text("( ͡° ͜ʖ ͡°)")
o.add(map, coords[0], coords[1])

map.show(init=True)

def move_object(obj:Text | Object, direction:str):
    global map
    if direction == "left":
        while obj.x <= 0:
            #obj.move(x=-1)
            obj.set(x=obj.x-1, y=obj.y)
            map.show()
    if direction == "right":
        while obj.x >= screen_width-len(obj.text):
            #obj.move(x=1)
            obj.set(x=obj.x+1, y=obj.y)
            map.show()
    if direction == "up":
        while obj.y <= 0:
            #obj.move(y=-1)
            obj.set(x=obj.x, y=obj.y-1)
            map.show()
    if direction == "down":
        while obj.y >= screen_height-3:
            #obj.move(y=1)
            obj.set(x=obj.x, y=obj.y+1)
            map.show()
    obj.remove()
    map.show()
        

def on_press(key:keyboard.KeyCode | keyboard.Key):
    global projectiles, current_key, coords
    try:
        k = key.char
    except:
        k = key.name
    if k not in current_key:
        current_key.add(k)
    if all(k in current_key for k in l_combination):
        projectile = Text(text="<-")
        projectile.add(map, o.x-1, o.y)
    elif all(k in current_key for k in r_combination):
        projectile = Text(text="->")
        projectile.add(map, o.x+len(o.text)+1, o.y)
    elif all(k in current_key for k in u_combination):
        projectile = Text(text="^\n|")
        projectile.add(map, o.x, o.y-1)
    elif all(k in current_key for k in d_combination):
        projectile = Text(text="|\nV")
        projectile.add(map, o.x, o.y+2)
    match k:
        case "a":
            if not coords[0] <= 0:
                coords[0] -= 1
        case "d":
            if not coords[0] >= screen_width-len(o.text):
                coords[0] += 1
        case "w":
            if not coords[1] <= 0:
                coords[1] -= 1
        case "s":
            if not coords[1] >= screen_height-2:
                coords[1] += 1
    o.set(coords[0], coords[1])
    map.show()

def on_release(key:keyboard.Key | keyboard.KeyCode):
    try:
        k = key.char
    except:
        k = key.name
    if k in current_key:
        current_key.remove(k)

listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    getpass(prompt="")

listener.join()
