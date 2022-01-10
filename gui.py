import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
from app import *
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"

class GuiApp:
    def __init__(self, master=None):

        self.system_raw = ""
        # build ui
        self.main = tk.Tk() if master is None else tk.Toplevel(master)
        self.title = ttk.Label(self.main)
        self.title.configure(font='{Calibri} 14 {bold}', text='Commander dashboard')
        self.title.grid(column='3', padx='0', pady='5', row='1')
        self.lbl_system_now = ttk.Label(self.main)
        self.actuel_sys = tk.StringVar(value='Système actuel :')
        self.lbl_system_now.configure(font='{Calibri} 12 {}', text='Système actuel :', textvariable=self.actuel_sys)
        self.lbl_system_now.grid(column='1', ipady='50', padx='5', row='4', sticky='w')
        self.lbl_brut = ttk.Label(self.main)
        self.lbl_brut.configure(font='{Calibri} 12 {}', text='Trader matériaux brut :')
        self.lbl_brut.grid(column='1', padx='5', pady='5', row='5', sticky='w')
        self.main.rowconfigure('5', minsize='0', pad='0')
        self.lbl_fabr = ttk.Label(self.main)
        self.lbl_fabr.configure(font='{Calibri} 12 {}', text='Trader matériaux fabriqué :')
        self.lbl_fabr.grid(column='1', padx='5', pady='5', row='6', sticky='w')
        self.lbl_data = ttk.Label(self.main)
        self.lbl_data.configure(font='{Calibri} 12 {}', text='Trader donnée :')
        self.lbl_data.grid(column='1', padx='5', pady='5', row='7', sticky='w')
        self.label10 = ttk.Label(self.main)
        self.brut_trader = tk.StringVar(value=self.test())
        self.label10.configure(font='{Calibri} 12 {}', text='label10', textvariable=self.brut_trader)
        self.label10.grid(column='2', row='5', sticky='w')
        self.label11 = ttk.Label(self.main)
        self.fabr_trader = tk.StringVar(value='label10')
        self.label11.configure(font='{Calibri} 12 {}', text='label10', textvariable=self.fabr_trader)
        self.label11.grid(column='2', row='6', sticky='w')
        self.label12 = ttk.Label(self.main)
        self.data_trader = tk.StringVar(value='label10')
        self.label12.configure(font='{Calibri} 12 {}', text='label10', textvariable=self.data_trader)
        self.label12.grid(column='2', row='7', sticky='w')
        self.label13 = ttk.Label(self.main)
        self.brut_trader_station = tk.StringVar(value='label10')
        self.label13.configure(font='{Calibri} 12 {}', text='label10', textvariable=self.brut_trader_station)
        self.label13.grid(column='4', row='5', sticky='w')
        self.label14 = ttk.Label(self.main)
        self.fabr_trader_station = tk.StringVar(value='label10')
        self.label14.configure(font='{Calibri} 12 {}', text='label10', textvariable=self.fabr_trader_station)
        self.label14.grid(column='4', row='6', sticky='w')
        self.label15 = ttk.Label(self.main)
        self.data_trader_station = tk.StringVar(value='label10')
        self.label15.configure(font='{Calibri} 12 {}', text='label10', textvariable=self.data_trader_station)
        self.label15.grid(column='4', row='7', sticky='w')
        self.main.configure(height='200', width='200')
        self.main.geometry('640x480')
        self.main.resizable(False, False)

        # Main widget
        self.mainwindow = self.main

    def test(self):
        system_raw = get_trade_raw()[0]
        return system_raw

    def run(self):
        self.mainwindow.after(2000, self.test)
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = GuiApp()
    app.run()


