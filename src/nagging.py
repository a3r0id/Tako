import tkinter as tk
from tkinter import simpledialog, messagebox

ROOT = tk.Tk()
ROOT.withdraw()

class Nagging(object):

    def __init__(self, title, message):
        self.title    = "Tako: " + title
        self.message  = message

    def ask(self):
        return simpledialog.askstring(title=self.title, prompt=self.message)
    
    def error(self):
        messagebox.showerror(self.title, self.message)
    
    def info(self):
        messagebox.showinfo(self.title, self.message)

    def warning(self):
        messagebox.showwarning(self.title, self.message)