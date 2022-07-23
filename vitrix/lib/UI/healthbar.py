from vitrix_engine import *
from lib.data import GamePaths


class HealthBar(Entity):
    def __init__(self, max_value):
        cube = os.path.join(GamePaths.models_dir, "cube.obj")
        super().__init__(
            parent = camera.ui,
            position = Vec2(-.62, -.43),
            scale = Vec2(.4175, .125),
            rotation=Vec3(0, 0, 180),
            model = cube,
        )

        self.icon = Entity(parent=camera.ui, model=cube, position=Vec2(-.81, -.43),
                           texture=os.path.join(GamePaths.textures_dir, "heart.png"),
                           scale=0.1, shader=None)
        
        self.shader = None
        self.max_value = max_value
        self.value = self.max_value
        self.segments = 15
        self.value_per_segment = self.max_value / self.segments

        self.update_texture(self.value)

    def update_texture(self, value):
        if value > self.max_value:
            self.value = self.max_value
        else:
            self.value = value
        
        x = 0
        i = 0
        while x < self.value:
            x += self.value_per_segment
            i += 1
        self.texture = os.path.join(GamePaths.textures_dir, "healthbar",
                                    str(i) +".png")
        
    def update(self):
        self.update_texture(self.value)

