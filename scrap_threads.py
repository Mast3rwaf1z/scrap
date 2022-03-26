from concurrent.futures import thread
from time import sleep
import scrap_engine as engine
from threading import Thread, current_thread

log = open("log.txt", "w")

def threadmove(obj:engine.Object, y_pos):
    global map
    for _ in range(engine.screen_width-1):
        obj.remove()
        obj.add(map, obj.x-1, obj.y-y_pos)
        map.show()
        log.write(f'moved obj at {engine.screen_height+i} to {obj.x}x{obj.y}\n')
        sleep(.1)
    if not current_thread().name == "MainThread":
        log.write("finished thread\n")


map = engine.Map(background=" ")
map.show(init=True)
objs:list[engine.Object] = []
objs.append(engine.Object(char="t"))
for i in range(1):
    objs[len(objs)-1].add(map,engine.screen_width-1, engine.screen_height-2)
    threadmove(objs[len(objs)-1], i)
    sleep(1)
while True:
    map.show()