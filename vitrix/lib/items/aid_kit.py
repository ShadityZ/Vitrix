from vitrix_engine import *
from lib.data import GamePaths

class AidKit(Entity):
    def __init__(self, position: tuple):
        super().__init__(
            model=os.path.join(GamePaths.models_dir, "first_aid_kit.obj"),
            color=color.rgb(255, 0, 0), # red
            position=position,
            collider="sphere",
            scale=.4,
        )

        self.collider = MeshCollider(self)

class AidKitInHand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model=os.path.join(GamePaths.models_dir, "first_aid_kit.obj"),
            color=color.rgb(255, 0, 0), # red
            position=Vec2(.5, -.4),
            rotation=Vec3(-5, 220, 0),
            scale=.2,
        )

        self.collider = MeshCollider(self)
