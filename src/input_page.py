import tkinter as tk
from tkinter.filedialog import askopenfilename
from default_page import *

class Application(Default):
    def __init__(self, title):
        super().__init__(title)

    def create_widgets(self):
        #sensor data
        sensor_label = tk.Label(self, text='Sensors information', font=('Arial', 11))
        sensor_label.grid(row=10, column=0, padx=5, pady=10)
        sensor_textbox = tk.Entry(self, font=('Arial', 11))
        sensor_textbox.grid(row=10, column=1, padx=5, pady=10)
        def sensor_readfile():
            filename = askopenfilename()
            sensor_textbox.insert(0, str(filename))
        sensor_btn = tk.Button(self, command=sensor_readfile, text='select')
        sensor_btn.grid(row=10, column=2, padx=5, pady=10)
        #attribute data
        attribute_label = tk.Label(self, text='Attribute information', font=('Arial', 11))
        attribute_label.grid(row=20, column=0, padx=5, pady=10)
        attribute_textbox = tk.Entry(self, font=('Arial', 11))
        attribute_textbox.grid(row=20, column=1, padx=5, pady=10)
        def attribute_readfile():
            filename = askopenfilename()
            attribute_textbox.insert(0, str(filename))
        attribute_btn = tk.Button(self, command=attribute_readfile, text='select')
        attribute_btn.grid(row=20, column=2, padx=5, pady=10)
        #all sensors data
        all_sensors_label = tk.Label(self, text='All sensors information', font=('Arial', 11))
        all_sensors_label.grid(row=30, column=0, padx=5, pady=10)
        all_sensors_textbox = tk.Entry(self, font=('Arial', 11))
        all_sensors_textbox.grid(row=30, column=1, padx=5, pady=10)
        def all_sensors_readfile():
            filename = askopenfilename()
            all_sensors_textbox.insert(0, str(filename))
        all_sensors_btn = tk.Button(self, command=all_sensors_readfile, text='select')
        all_sensors_btn.grid(row=30, column=2, padx=5, pady=10)

        # read_file
        def read_csv():
            try:
                
                print('s')
            except:
                print("s")


            
        attribute_btn = tk.Button(self, command=read_csv, text='select')
        attribute_btn.grid(row=20, column=2, padx=5, pady=10)

    def new_window(self):
        new_app = Application('Please input data')
        new_app.mainloop()
        