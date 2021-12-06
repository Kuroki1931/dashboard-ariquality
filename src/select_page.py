import tkinter as tk
import pandas as pd
import default_page
import input_page

from default_page import *
from dateutil import parser
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class SelectPage(default_page.Default):
    def __init__(self, title, data):
        super().__init__(title)
        self.geometry("1200x700")
        self.data = data
        self.gragh_data = None
        self.IAQI_list = [0, 50, 100, 150, 200, 300, 400]
        self.O3_list = [0, 160, 200, 300, 400, 500, 1000]
        self.SO2_list = [0, 50, 150, 475, 800, 1600, 2100]
        self.NO2_list = [0, 40, 80, 180, 280, 565, 750]
        self.PM10_list = [0, 50, 150, 250, 350, 420, 500]
        self.create_widgets()
        

    def create_widgets(self):
        # menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Input", command=self.new_window)
        filemenu.add_separator()
        menubar.add_cascade(label="Menu", menu=filemenu)
        self.config(menu=menubar)

        # data duration
        start_date = str(self.data.iloc[0, 0])[:10]
        end_date = str(self.data.iloc[-1, 0])[:10]
        start_label = tk.Label(self, text='data duration {}  -  {}'.format(start_date, end_date), font=('Arial', 11))
        start_label.grid(row=1, column=0, padx=1, pady=1)

        # Basic settings
        mean_label = tk.Label(self, text='Basic Settings', font=('Arial', 11), fg='blue')
        mean_label.grid(row=2, column=0, padx=1, pady=1)
        meanspan_label = tk.Label(self, text='mean span', font=('Arial', 11))
        meanspan_label.grid(row=3, column=0, padx=1, pady=1)
        chk = tk.Checkbutton(self, text='24 hour')
        chk.grid(row=3, column=1, padx=1, pady=1)
        standardday_label = tk.Label(self, text='standard day', font=('Arial', 11))
        standardday_label.grid(row=4, column=0, padx=1, pady=1)
        standardday_textbox = tk.Entry(self, font=('Arial', 11))
        standardday_textbox.grid(row=4, column=1, padx=1, pady=1)
        timespan_label = tk.Label(self, text='time span', font=('Arial', 11))
        timespan_label.grid(row=5, column=0, padx=1, pady=1)
        timespan_textbox = tk.Entry(self, font=('Arial', 11))
        timespan_textbox.grid(row=5, column=1, padx=1, pady=1)

        def excute():
            standard = standardday_textbox.get()
            timespan = int(timespan_textbox.get())
            data = self.data.copy()
            base = data['Timestamp'][0]
            data['Timestamp'] = data['Timestamp'] - base
            data['Timestamp'] = data['Timestamp'].apply(lambda x: x.days)
            data['O3'] = data['O3'].astype(float)
            data['NO2'] = data['NO2'].astype(float)
            data['SO2'] = data['SO2'].astype(float)
            data['PM10'] = data['PM10'].astype(float)
            standard_day = int((parser.parse(standard) - base).days)
            data = data.groupby(['Timestamp','SensorID']).mean()
            data = data.reset_index()
            extract_day_list = [i for i in range(standard_day-timespan, standard_day+timespan)]
            data = data[data['Timestamp'].isin(extract_day_list)]
            data['IAQI_O3'] = data['O3'].apply(lambda x: self.calculate_IAQI(self.IAQI_list, self.O3_list, x))
            data['IAQI_SO2'] = data['SO2'].apply(lambda x: self.calculate_IAQI(self.IAQI_list, self.SO2_list, x))
            data['IAQI_NO2'] = data['NO2'].apply(lambda x: self.calculate_IAQI(self.IAQI_list, self.NO2_list, x))
            data['IAQI_PM10'] = data['PM10'].apply(lambda x: self.calculate_IAQI(self.IAQI_list, self.PM10_list, x))
            data['AQI'] = data[['IAQI_O3', 'IAQI_SO2', 'IAQI_NO2', 'IAQI_PM10']].max(axis=1)
            self.gragh_data = data
        
        mean_btn = tk.Button(self, command=excute, text='read')
        mean_btn.grid(row=6, column=0, padx=5, pady=5)

        # gragh 
        frame = tk.Frame(self, width=200, height=100, relief=tk.GROOVE)
        frame.grid(row=0, column=1)
        fig = self.plot_wave(0, 0)
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().grid(row=0, column=0)

        # Gragh settings
        gragh_label = tk.Label(self, text='Gragh Settings', font=('Arial', 11), fg='blue')
        gragh_label.grid(row=7, column=0, padx=1, pady=1)
        area_label = tk.Label(self, text='area', font=('Arial', 11))
        area_label.grid(row=8, column=0, padx=1, pady=1)
        area_textbox = tk.Entry(self, font=('Arial', 11))
        area_textbox.grid(row=8, column=1, padx=1, pady=1)

        # gragh create
        def button1():
            area = area_textbox.get()
            data = self.gragh_data.copy()
            data = data[data['SensorID']==area]
            x = data['Timestamp']
            y = data['AQI']
            fig = self.plot_wave(x, y)
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0)

        gragh_btn = tk.Button(self, command=button1, text='create')
        gragh_btn.grid(row=9, column=0, padx=5, pady=5)    

    def calculate_IAQI(self, list1, list2, value):
            C_p = value
            for i in range(len(list2)-1):
                if (C_p>list2[i]) & (C_p<list2[i+1]):
                    BP_Hi = list2[i+1]
                    BP_Lo = list2[i]
                    IAQI_Hi = list1[i+1]
                    IAQI_Lo = list1[i]
                    return (IAQI_Hi - IAQI_Lo)/(BP_Hi-BP_Lo)*(C_p-BP_Lo)+IAQI_Lo

    def plot_wave(self, x, y):
        # Figureインスタンスを生成する。
        fig = plt.Figure()
    
        # 目盛を内側にする。
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
    
        # Axesを作り、グラフの上下左右に目盛線を付ける。
        ax1 = fig.add_subplot(111)
        ax1.yaxis.set_ticks_position('both')
        ax1.xaxis.set_ticks_position('both')
    
        # 軸のラベルを設定する。
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
    
        # データをプロットする。
        ax1.plot(x, y)
        return fig

    def new_window(self):
        new_app = input_page.InputPage('Please input data')
        new_app.mainloop()

    
        