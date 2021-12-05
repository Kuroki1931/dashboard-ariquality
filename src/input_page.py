import tkinter as tk
from tkinter.filedialog import askopenfilename
from default_page import *

class Application(Default):
    def __init__(self):
        super().__init__()

    def create_widgets(self):
        quit_btn = tk.Button(self)
        quit_btn['text'] = '閉じる'
        quit_btn['command'] = self.read_csv
        quit_btn.pack(side='bottom')

    def new_window(self):
        new_app = Application()
        new_app.mainloop()

    def read_csv(self):
        filename = askopenfilename()
        print(filename)