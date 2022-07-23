import os
from vitrix_engine import *
from lib.data import GamePaths

class Hammer(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            position = Vec2(.19, -.39),
            scale=0.1,
            rotation=Vec3(-20, -20, -5),
            model=os.path.join(GamePaths.models_dir, "hammer.obj"),
            texture=os.path.join(GamePaths.textures_dir, "hammer.png"),
            color=color.color(0, 0, .4),
            on_cooldown=False
        )