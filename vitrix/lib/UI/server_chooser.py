import os
from tkinter import *
from lib.data import GamePaths
from lib.UI.notification import notify


root = Tk()
root.title("Vitrix - Join a multiplayer server")

try:
    root.iconbitmap(os.path.join(GamePaths.static_dir, "logo.ico"))
except:
    pass

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 459
window_height = 150

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


def on_closing():
    os._exit(0)


def submit():
    try:
        temp =int(E3.get())
    except:
        notify("Vitrix Fatal Error", "Invalid Port Number!")
        return

    if E1.get().strip() != "":
        if E2.get().strip() != "":
            if E3.get().strip() != "":
                file = open("data.txt", "w")
                file.writelines([E1.get(), "\n",  E2.get(), "\n",  E3.get()])
                file.close()
                root.destroy()
            else:
                notify("Vitrix Fatal Error", "Port cannot be blank!")
                return
        else:
            notify("Vitrix Fatal Error", "IP Address cannot be blank!")
            return
    else:
        notify("Vitrix Fatal Error", "Username cannot be blank!")
        return
        
    

L1 = Label(root, text="Username:")
L1.place(anchor = CENTER, relx = .10, rely = .1)
E1 = Entry(root, bd = 5)
E1.place(anchor = CENTER, relx = .5, rely = .1)

L2 = Label(root, text="Server:")
L2.place(anchor = CENTER, relx = .10, rely = .3)
E2 = Entry(root, bd = 5)
E2.place(anchor = CENTER, relx = .5, rely = .3)

L3 = Label(root, text="Port:")
L3.place(anchor = CENTER, relx = .10, rely = .5)
E3 = Entry(root, bd = 5)
E3.place(anchor = CENTER, relx = .5, rely = .5)

submit = Button(root, text="Join", width=10, command=submit)
submit.place(anchor = CENTER, relx = .5, rely = .8)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
