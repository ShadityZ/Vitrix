from numpy import identity
from vitrix_engine import *
from lib.data import GamePaths, Items

class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (5, 3),
            scale = (.5, .3),
            origin = (-.5, .5),
            position = (-.28, -.4),
            color = color.color(0, 0, .1),
            )
        self.shader = None
        self.shown = False
        
        self.items = [
            [["empty", 0], ["empty", 0], ["empty", 0], ["empty", 0], ["empty", 0]],
            [["empty", 0], ["empty", 0], ["empty", 0], ["empty", 0], ["empty", 0]],
            [["empty", 0], ["empty", 0], ["empty", 0], ["empty", 0], ["empty", 0]]
        ]

        self.entities = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]

    
    def find_free_spot(self):
        y = 0
        for items in self.items:
            x = 0
            for item in items:
                if item[0] == "empty":
                    return y, x
                x += 1
            y += 1


    def find_item(self, id: str):
        y = 0
        for items in self.items:
            x = 0
            for item in items:
                if item[0] == id:
                    return y, x, item[1]
                x += 1
            y += 1
        return False


    def append(self, id: str, amount: int = 1):
        if self.find_item(id) != False and not (id in Items.nonstackable_items):
            column, row, temp = self.find_item(id)
            self.items[column][row][1] += amount
            icon = self.entities[column][row]
            name = id.replace('_', ' ').title()
            icon.tooltip.text = f"{name} x{self.items[column][row][1]}"
        else:
            try:
                column, row = self.find_free_spot()
            except:
                return False
            
            self.items[column][row][0] = id
            self.items[column][row][1] = amount

            icon = Draggable(
                parent = self,
                model = os.path.join(GamePaths.models_dir, "cube.obj"),
                texture = os.path.join(GamePaths.textures_dir, "items", f"{id}.png"),
                color = color.white,
                scale_x = 1/self.texture_scale[0],
                scale_y = 1/self.texture_scale[1],
                origin = (-.5, .5),
                x = row * 1/self.texture_scale[0],
                y = -column * 1/self.texture_scale[1],
                z = -.5,
            )
            name = id.replace('_', ' ').title()

            icon.tooltip = Tooltip(f"{name} x1")
            icon.tooltip.background.color = color.color(0, 0, 0, .8)
            icon.org_x = row,
            icon.org_y = column,
            icon.new_x = None,
            icon.new_y = None,

            def drag():
                icon.org_pos = (icon.x, icon.y)
                icon.z -= .01

            def drop():
                icon.x = int((icon.x + (icon.scale_x/2)) * 5) / 5
                icon.y = int((icon.y - (icon.scale_y/2)) * 3) / 3
                #icon.org_x = int(int(str(icon.org_pos[0])[2])/2)
                icon.new_x = int(int(str(icon.x)[2])/2)

                #try:
                #    icon.org_y = int(int(str(icon.org_pos[1])[3])/3)
                #except:
                #    icon.org_y = int(int(str(icon.org_pos[1])[2])/3)

                try:
                    icon.new_y = int(int(str(icon.y)[3])/3)
                except:
                    icon.new_y = int(int(str(icon.y)[2])/3)




                icon.z += .01

                if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                    icon.position = (icon.org_pos)
                    return

                for columns in self.entities:
                    for entity in columns:
                        if entity == icon:
                            continue
                        try:
                            if entity.x == icon.x and entity.y == icon.y:
                                entity.position = icon.org_pos
                        except:
                            pass


            icon.drag = drag
            icon.drop = drop

            self.entities[column][row] = icon

    def remove(self, id: str, amount: int = 1):
        try:
            column, row, temp = self.find_item(id)
        except:
            return False
        if (self.items[column][row][1] - amount) <= 0:
            self.items[column][row][0] = "empty"
            self.items[column][row][1] = 0
            destroy(self.entities[column][row])
            self.entities[column][row] = None
            return
        
        self.items[column][row][1] -= amount
        icon = self.entities[column][row]
        name = id.replace('_', ' ').title()
        icon.tooltip = Tooltip(f"{name} x1")

        self.entities[column][row] = icon
    
    def update(self):
        for row in self.entities:
            for item in row:
                try:
                    if (item.new_x != (None,)) and (item.new_y != (None,)):
                        org_item = self.items[item.org_y[0]][item.org_x[0]]
                        self.items[item.org_y[0]][item.org_x[0]] = ["empty", 0]

                        item.org_x = item.new_x
                        item.org_y = item.new_y

                        self.items[item.org_y][item.org_x] = org_item

                        item.new_x = None
                        item.new_y = None

                        print(self.items)
                except:
                    pass

