import tkinter as tk
from tkinter import ttk

from src.constants import CELL_MIN_PX_SIZE


class SimulationSettings:
    def __init__(self):
        self._root: tk.Tk = None
        self._resolution_var: tk.StringVar = None
        self._fullscreen_var: tk.BooleanVar = None
        self._statistics_var: tk.BooleanVar = None

        self.fullscreen: bool = None
        self.statistics: bool = None

        self.screen_width: int = None
        self.screen_height: int = None

        self.screen_pond_width: int = None
        self.screen_pond_height: int = None

        self.pond_width: int = None
        self.pond_height: int = None

    def get_user_settings(self) -> None:
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.geometry("350x250")

        self._root.columnconfigure(0, weight=1)
        self._root.columnconfigure(1, weight=2)

        self._add_resolution_setting(0)
        self._add_fullscreen_setting(1)
        self._add_statistics_setting(2)
        self._add_empty_pond_setting(3)
        self._add_no_worms_from_heaven_setting(4)

        tk.Button(
            self._root, text="Run simulation", command=self._apply_settings
        ).grid(row=5, column=0, columnspan=2)

        # There are a few rows with 2 widgets and one with 1 widget
        for i in range((len(self._root.winfo_children()) + 1) // 2):
            self._root.rowconfigure(i, weight=1)

        for child in self._root.winfo_children():
            child.grid_configure(padx=10)

        self._root.mainloop()

    def _add_resolution_setting(self, row):
        tk.Label(self._root, text='Resolution: ').grid(row=row, column=0, sticky='w')
        self._resolution_var = tk.StringVar()
        resolution = ttk.Combobox(self._root, textvariable=self._resolution_var)
        resolution['values'] = ('1920x1080', '1080x720', '720x480')
        resolution['state'] = 'readonly'
        resolution.current(1)
        resolution.grid(row=row, column=1, sticky='we')

    def _add_fullscreen_setting(self, row):
        tk.Label(self._root, text='Full screen mode: ').grid(row=row, column=0, sticky='w')
        self._fullscreen_var = tk.BooleanVar()
        fullscreen = tk.Checkbutton(self._root, variable=self._fullscreen_var)
        fullscreen.grid(row=row, column=1, sticky='we')

    def _add_statistics_setting(self, row):
        tk.Label(self._root, text='Show statistics: ').grid(row=row, column=0, sticky='w')
        self._statistics_var = tk.BooleanVar()
        statistics = tk.Checkbutton(self._root, variable=self._statistics_var)
        statistics.grid(row=row, column=1, sticky='we')

    def _add_empty_pond_setting(self, row):
        tk.Label(self._root, text='Empty pond: ').grid(row=row, column=0, sticky='w')
        self._empty_pond_setting_var = tk.BooleanVar()
        empty_pond_setting = tk.Checkbutton(self._root, variable=self._empty_pond_setting_var)
        empty_pond_setting.grid(row=row, column=1, sticky='we')

    def _add_no_worms_from_heaven_setting(self, row):
        tk.Label(self._root, text='No worms from heaven: ').grid(row=row, column=0, sticky='w')
        self._no_worms_from_heaven_var = tk.BooleanVar()
        no_worms_from_heaven = tk.Checkbutton(self._root, variable=self._no_worms_from_heaven_var)
        no_worms_from_heaven.grid(row=row, column=1, sticky='we')

    def _apply_settings(self) -> None:
        res = self._resolution_var.get().split('x')
        self.screen_width = int(res[0])
        self.screen_height = int(res[1])

        self.fullscreen = self._fullscreen_var.get()
        self.statistics = self._statistics_var.get()
        self.empty_pond_setting = self._empty_pond_setting_var.get()
        self.no_worms_from_heaven = self._no_worms_from_heaven_var.get()

        self.screen_pond_width = self.screen_width
        self.screen_pond_height = int(self.screen_height * 0.9)
        self.screen_pond_height -= self.screen_pond_height % CELL_MIN_PX_SIZE

        self.pond_width = self.screen_pond_width // CELL_MIN_PX_SIZE
        self.pond_height = self.screen_pond_height // CELL_MIN_PX_SIZE

        self._root.destroy()
