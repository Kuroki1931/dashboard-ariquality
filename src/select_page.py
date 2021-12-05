import tkinter as tk
import pandas as pd
from default_page import *
import default_page
import input_page


class SelectPage(default_page.Default):
    def __init__(self, title):
        super().__init__(title)
        self.geometry("1000x700")
        self.create_widgets()

    def create_widgets(self):
        # menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Input", command=self.new_window)
        filemenu.add_separator()
        menubar.add_cascade(label="Menu", menu=filemenu)
        self.config(menu=menubar)

    def new_window(self):
        new_app = input_page.InputPage('Please input data')
        new_app.mainloop()
        