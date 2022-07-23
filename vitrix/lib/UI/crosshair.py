from vitrix_engine import *
from lib.data import GamePaths


class Crosshair(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model=os.path.join(GamePaths.models_dir, "cube.obj"),
            scale=.07
        )
        self.shader = None
        self.set_ranged()

    def set_ranged(self):
        self.texture = os.path.join(GamePaths.textures_dir, "ranged-crosshair.png")

    def set_melee(self):
        self.texture = os.path.join(GamePaths.textures_dir, "melee-crosshair.png")