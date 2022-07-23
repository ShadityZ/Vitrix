import os
from vitrix_engine import *
from lib.data import GamePaths

class BattleAxe(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            position = Vec2(.7, -.3),
            scale=.05,
            rotation=Vec3(-20, -20, -10),
            model=os.path.join(GamePaths.models_dir, "battleaxe.obj"),
            #texture=os.path.join(GamePaths.textures_dir, "axe.png"),
            color=color.color(0, 0, .4),
            on_cooldown=False
        )