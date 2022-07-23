import os
from vitrix_engine import *
from lib.data import GamePaths

class Sword(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            position = Vec2(.6, -.39),
            scale=0.1,
            rotation=Vec3(120, 60, 50),
            model=os.path.join(GamePaths.models_dir, "sword.obj"),
            #texture=os.path.join(GamePaths.textures_dir, "sword.png"),
            color=color.color(0, 0, .4),
            on_cooldown=False
        )