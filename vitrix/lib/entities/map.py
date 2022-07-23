import os
from vitrix_engine import *

from lib.data import GamePaths
from lib.entities.crate import Crate


class FloorCube(Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model=os.path.join(GamePaths.models_dir, "cube.obj"),
            texture=os.path.join(GamePaths.textures_dir, "floor.png"),
            collider="box"
        )


class Map(Entity):
    def __init__(self):
        super().__init__(
            model=os.path.join(GamePaths.models_dir, "map1.obj"),
            scale=.3
        )
        self.collider = MeshCollider(self)
        self.crate_one = Crate(position=Vec3(10, 1, -5))
        self.sky = Entity(
            model=os.path.join(GamePaths.models_dir, "sphere.obj"),
            texture=os.path.join(GamePaths.textures_dir, "sky.png"),
            scale=9999,
            double_sided=True
        )

        # Floor
        dark1 = True
        for z in range(-28, 30, 2):
            dark2 = not dark1

            for x in range(-18, 28, 2):
                cube = FloorCube(Vec3(x, 0, z))

                if dark2:
                    cube.color = color.color(0, .2, .8)
                else:
                    cube.color = color.color(0, .2, 1)
                
                dark2 = not dark2
            
            dark1 = not dark1