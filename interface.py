# interface.py

import tkinter as tk
from tkinter import messagebox, simpledialog

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
