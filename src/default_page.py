import tkinter as tk

class Default(tk.Tk):
    def __init__(self, title=None):
        super().__init__()
        self.create_widgets()
        self.title('Air quality')
        self.geometry("400x300")
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Input", command=self.new_window)
        filemenu.add_separator()
        menubar.add_cascade(label="Menu", menu=filemenu)
        self.config(menu=menubar)
        label = tk.Label(self, text=title, font=('Arial', 14))
        label.grid(row=0, column=0, padx=5, pady=10)
        self.sensor_data
        self.attribute_data
        self.all_sensor_data
