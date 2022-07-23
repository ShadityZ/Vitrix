import os

class GamePaths:
    models_dir = os.path.join("assets", "models")
    textures_dir = os.path.join("assets", "textures")
    sounds_dir = os.path.join("assets", "sounds")
    static_dir = os.path.join("assets", "static")

    server_dir = os.path.join("..", "server")


class Items:
    nonstackable_items = ["pistol", "hammer", "sword", "battleaxe"]
