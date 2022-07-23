import os
import tkinter as tk
from lib.data import GamePaths

def on_closing():
    os._exit(0)

def notify(title: str, msg: str,):
    popup = tk.Tk()
    popup.title(title)
    try:
        popup.iconbitmap(os.path.join(GamePaths.static_dir, "logo.ico"))
    except:
        pass
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack(pady=10)
    popup.protocol("WM_DELETE_WINDOW", on_closing)
    popup.mainloop()
