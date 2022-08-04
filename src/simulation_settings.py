import tkinter as tk
from tkinter import ttk

from src.constants import CELL_MIN_PX_SIZE


class SimulationSettings:
    def __init__(self):
        self._root: tk.Tk
        self._resolution_var: tk.StringVar
        self._fullscreen_var: tk.BooleanVar

        self.screen_width: int
        self.screen_height: int

        self.fullscreen: bool

        self.screen_pond_width: int
        self.screen_pond_height: int

        self.pond_width: int
        self.pond_height: int

    def get_user_settings(self) -> None:
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.geometry("350x200")

        self._root.columnconfigure(0, weight=1)
        self._root.columnconfigure(1, weight=2)

        self._add_resolution_setting()
        self._add_fullscreen_setting()

        tk.Button(
            self._root, text="Run simulation", command=self._apply_settings
        ).grid(row=2, column=0, columnspan=2)

        # There are a few rows with 2 widgets and one with 1 widget
        for i in range((len(self._root.winfo_children()) + 1) // 2):
            self._root.rowconfigure(i, weight=1)

        for child in self._root.winfo_children():
            child.grid_configure(padx=10, pady=10)

        self._root.mainloop()

    def _add_resolution_setting(self):
        tk.Label(self._root, text='Resolution: ').grid(row=0, column=0, sticky='w')
        self._resolution_var = tk.StringVar()
        resolution = ttk.Combobox(self._root, textvariable=self._resolution_var)
        resolution['values'] = ('1920x1080', '1080x720', '720x480')
        resolution['state'] = 'readonly'
        resolution.current(1)
        resolution.grid(row=0, column=1, sticky='we')

    def _add_fullscreen_setting(self):
        tk.Label(self._root, text='Full screen mode: ').grid(row=1, column=0, sticky='w')
        self._fullscreen_var = tk.BooleanVar()
        fullscreen = tk.Checkbutton(self._root, variable=self._fullscreen_var)
        fullscreen.grid(row=1, column=1, sticky='we')

    def _apply_settings(self) -> None:
        res = self._resolution_var.get().split('x')
        self.screen_width = int(res[0])
        self.screen_height = int(res[1])

        self.fullscreen = self._fullscreen_var.get()

        self.screen_pond_width = self.screen_width
        self.screen_pond_height = int(self.screen_height * 0.9)
        self.screen_pond_height -= self.screen_pond_height % CELL_MIN_PX_SIZE

        self.pond_width = self.screen_pond_width // CELL_MIN_PX_SIZE
        self.pond_height = self.screen_pond_height // CELL_MIN_PX_SIZE

        self._root.destroy()
