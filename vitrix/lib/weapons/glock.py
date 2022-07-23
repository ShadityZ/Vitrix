import os
from vitrix_engine import *
from lib.data import GamePaths

class Pistol(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            position = Vec2(0.8, -.6),
            scale=0.07,
            rotation=Vec3(-10, 20, 5),
            model=os.path.join(GamePaths.models_dir, "glock.obj"),
            texture=os.path.join(GamePaths.textures_dir, "glock.png"),
            color=color.color(0, 0, .4),
            on_cooldown=False
        )