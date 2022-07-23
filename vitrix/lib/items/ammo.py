from vitrix_engine import *
from lib.data import GamePaths

class Ammo(Entity):
    def __init__(self, position: tuple):
        super().__init__(
            model=os.path.join(GamePaths.models_dir, "ammo.obj"),
            texture=os.path.join(GamePaths.textures_dir, "ammo.png"),
            position=position,
            scale=.4,
        )

        self.collider = MeshCollider(self)


class AmmoInHand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model=os.path.join(GamePaths.models_dir, "ammo.obj"),
            texture=os.path.join(GamePaths.textures_dir, "ammo.png"),
            position=Vec2(.6, -.48),
            rotation=Vec3(-5, 50, 20),
            scale=.15,
        )

        self.collider = MeshCollider(self)
