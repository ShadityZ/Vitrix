import os
from vitrix_engine import *

from lib.entities.map import Map
from lib.entities.player import Player
from lib.entities.enemy import Zombie

from lib.items.aid_kit import AidKit
from lib.items.ammo import Ammo

from lib.data import GamePaths
from vitrix_engine.shaders.basic_lighting_shader import basic_lighting_shader
from lib.api.settings import *

window.title = "Vitrix - Singleplayer"
window.icon = os.path.join(GamePaths.static_dir, "logo.ico")

app = Ursina()
# The inventory needs to load after ursina app()
#from lib.UI.inventory import *

window.borderless = False
window.exit_button.visible = False
default_width = sread('game_settings', 'window_width')
default_height = sread('game_settings', 'window_height')
window.size = (default_width, default_height)
# window.fullscreen = True

try:
    from colorama import Fore
    print("\n" + Fore.CYAN + "Toggle fullscreen with F11 to get better performances" + Fore.RESET)
except:
    print("Please install colorama to see colorized text")
    print("Toggle fullscreen with F11 to get better performances")

Text.default_font = os.path.join(GamePaths.static_dir, "font.ttf")
if sread('gameplay_settings', 'shadows') == "True":
    Entity.default_shader = basic_lighting_shader
    sun = DirectionalLight()
    sun.look_at(Vec3(1,-1,-1))

map = Map()

def toggle_fullscreen():
    if window.fullscreen:
        window.fullscreen = False
    else:
        window.fullscreen = True

fullscreen_button = Button(
            text="Toggle Fullscreen",
            position=Vec2(.2, 0),
            scale=0.15,
            enabled=False,
            on_click=Func(toggle_fullscreen)
        )
fullscreen_button.fit_to_text()


player = Player(Vec3(0, 1, 0))
aid_kit = AidKit(Vec3(10, 1.4, 3))
ammo = Ammo(Vec3(15, 1, 3))

camera.fov = int(sread('gameplay_settings', 'fov'))

enemies = []


#controls_dict={
#    "tab":"Pause the Game",
#    "L":"Release a zombie",
#    "left-click":"Fire",
#    "space": "Jump",
#    "alt-f4":"Exit game",
#    "1":"Switch ammo"
#}
#controls_text = Text(
#                text= "".join(f"{key} = {value}\n" for key,value in controls_dict.items() ),
#                origin=Vec2(2.8, -3),
#                scale=1
#                )
#def cycleAmmo(bullet_tag):  # default bullet tag is int 1
#    if bullet_tag == 1:
#        return 2
#    else:
#        return 1


def input(key):
    if key == ("tab" or "escape"):
        if player.paused:
            player.pause_text.disable()
            player.exit_button.disable()
            fullscreen_button.disable()
            player.crosshair.enable()
            player.paused = False
            player.on_enable()
        else:
            player.pause_text.enable()
            player.exit_button.enable()
            fullscreen_button.enable()
            player.crosshair.disable()
            player.paused = True
            player.on_disable()
    
    if key == "l":
        enemies.append(Zombie(Vec3(0, 1.5, 0), player))


if __name__ == "__main__":
    app.run(info=False)
