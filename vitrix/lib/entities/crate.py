import os
from vitrix_engine import *
import random

from lib.data import GamePaths


class Crate(Entity):

    def __init__(self, position):
        super().__init__(
            position=position,
            scale=1.5,
            origin_y=-.5,
            model=os.path.join(GamePaths.models_dir, "cube.obj"),
            texture=os.path.join(GamePaths.textures_dir, "crate.png"),
        )
        
        items_list = ["pistol", "pistol", "pistol", "pistol", "sword", "sword", "battleaxe", "nothing", 
                      "nothing", "nothing"]

        self.contents = []

        self.collider = BoxCollider(self, size=Vec3(1, 2, 1))
        for i in range (1, random.randint(2, 4)):
            self.contents.append(random.choice(items_list))

        

