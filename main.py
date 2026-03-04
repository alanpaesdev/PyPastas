# main.py
import tkinter as tk
from ui.app import LifeOSApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeOSApp(root)
    root.mainloop()