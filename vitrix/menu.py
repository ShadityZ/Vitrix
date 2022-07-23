import os, platform, threading, requests
from vitrix_engine import *
from lib.api.settings import *

def get_last_version():
    try:
        r = requests.get("https://raw.githubusercontent.com/ShadityZ/Vitrix/dev/vitrix/version.txt")
        return r.text
    except:
        return "unknown"


def buildexec(modulename, dir_path):
    try:
        if modulename == "mp":
            os.system("python " + dir_path + "/multiplayer.py")
        elif modulename =="sp":
            os.system("python " + dir_path + "/singleplayer.py")
        else:
            pass
    except:
        pass


def start_multiplayer():
    app.destroy()
    if built:
        if platform.system() == "Linux":
            os.system("sh multiplayer.sh")
        if platform.system() == "Windows":
            os.system("multiplayer.bat")
    else:
        buildexec("mp", dir_path)
    os._exit(0)

def start_singleplayer():
    app.destroy()
    if built:
        if platform.system() == "Linux":
            os.system("sh singleplayer.sh")
        if platform.system() == "Windows":
            os.system("singleplayer.bat")
    else:
        buildexec("sp", dir_path)
    os._exit(0)


def playBackgroundMusic():
    global bgmusic
    bgmusic = Audio("background-music")
    bgmusic.loop = True
    bgmusic.play()


class LoadingWheel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.point = Entity(parent=self, model=Circle(24, mode='point', thickness=.03),
                            color=color.light_gray, y=.75, scale=2, texture='circle')
        self.point2 = Entity(parent=self, model=Circle(12, mode='point', thickness=.03),
                             color=color.light_gray, y=.75, scale=1, texture='circle')

        self.scale = .025
        self.text_entity = Text(world_parent=self, text='Loading...', origin=(0,1.5),
                                color=color.light_gray)
        self.y = -.25

        self.bg = Entity(parent=self, model='quad', scale_x=camera.aspect_ratio,
                         color=color.black, z=1)
        self.bg.scale *= 400

        for key, value in kwargs.items():
            setattr(self, key ,value)


    def update(self):
        self.point.rotation_y += 5
        self.point2.rotation_y += 3


class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, scale=(.25, .075), highlight_color=color.gray, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)

def back_settings(fov: str):
    global state_handler
    swrite("gameplay_settings", "fov", str(fov))
    setattr(state_handler, 'state', 'main_menu')

def toggle_shaders():
    global shaders_button
    button = shaders_button
    if sread("gameplay_settings", "shadows") == "true":
        swrite("gameplay_settings", "shadows", "False")
        button.text_entity.text = "Shadows: Off"
    else:
        swrite("gameplay_settings", "shadows", "True")
        button.text_entity.text = "Shadows: On"

def load_menu():
    global state_handler
    button_spacing = .075 * 1.25
    menu_parent = Entity(parent=camera.ui, y=.15)
    main_menu = Entity(parent=menu_parent)
    load_menu = Entity(parent=menu_parent)
    options_menu = Entity(parent=menu_parent)


    state_handler = Animator({
        'main_menu' : main_menu,
        'load_menu' : load_menu,
        'options_menu' : options_menu,
        }
    )


    main_menu.buttons = [
        MenuButton('Start', on_click=Func(setattr, state_handler, 'state', 'load_menu')),
        MenuButton('Options', on_click=Func(setattr, state_handler, 'state', 'options_menu')),
        MenuButton('Quit', on_click=Sequence(Wait(.01), Func(sys.exit))),
    ]
    for i, e in enumerate(main_menu.buttons):
        e.parent = main_menu
        e.y = (-i-2) * button_spacing
        e.enabled = False

    singleplayer_btn = MenuButton(parent=load_menu, text="Singleplayer",
                                  on_click=Func(start_singleplayer), y=(i*button_spacing))

    multiplayer_btn = MenuButton(parent=load_menu, text="Multiplayer",
                                  on_click=Func(start_multiplayer), y=((i-1)*button_spacing))

    load_menu.back_button = MenuButton(parent=load_menu, text='back',
                                       y=((-i-2)*button_spacing),
                                    on_click=Func(setattr, state_handler,
                                                  'state', 'main_menu'))

    for t in [e for e in scene.entities if isinstance(e, Text)]:
        t.original_scale = t.scale

    fov_slider = Slider(20, 130, default=int(sread("gameplay_settings", "fov")), step=1, dynamic=True, 
                        text='FOV:   ', parent=options_menu)
    if sread("gameplay_settings", "shadows") == "true":
        button_text = "Shadows: On"
    else:
        button_text = "Shadows: Off"

    global shaders_button
    shaders_button = Button(text=button_text, scale=0.15, parent=options_menu, on_click=Func(toggle_shaders))

    options_back = MenuButton(parent=options_menu, text='Back', x=-.25, origin_x=-.5,
                            on_click=Func(back_settings, str(fov_slider.value)))

    for i, e in enumerate((fov_slider, shaders_button, options_back)):
        e.y = -i * button_spacing


    for menu in (main_menu, load_menu, options_menu):
        def animate_in_menu(menu=menu):
            for i, e in enumerate(menu.children):
                e.original_x = e.x
                e.x += .1
                e.animate_x(e.original_x, delay=i*.05, duration=.1,
                            curve=curve.out_quad) # type: ignore

                e.alpha = 0
                e.animate('alpha', .7, delay=i*.05, duration=.1,
                        curve=curve.out_quad) # type: ignore

                if hasattr(e, 'text_entity'):
                    e.text_entity.alpha = 0
                    e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

        menu.on_enable = animate_in_menu


    background = Entity(model="cube", texture='background', parent=camera.ui,
                        scale=(camera.aspect_ratio), color=color.white, z=1)


    playBackgroundMusic()
    print('Loaded Menu')
    loading_screen.enabled = False
    for i, e in enumerate(main_menu.buttons):
        e.enabled = True


window.title = "Vitrix - Menu"
app = Ursina()
loading_screen = LoadingWheel(enabled=False)
window.exit_button.visible = False
window.borderless = False
default_width = sread("game_settings", "window_width")
default_height = sread("game_settings", "window_height")
window.size = (default_width, default_height)
window.fullscreen = False

loading_screen.enabled = True
threading.Thread(target=load_menu).start()


dir_path = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(dir_path + "/.unbuilt"):
    built = False
else:
    built = True


if __name__ == "__main__":
    app.run(info=False)