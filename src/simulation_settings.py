import tkinter as tk
from tkinter import ttk

from src.constants import CELL_MIN_PX_SIZE


class SimulationSettings:
    def __init__(self):
        self._root = None
        self._resolution_val = None

    def get_user_settings(self) -> None:
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.geometry("300x200")

        self._root.columnconfigure(0, weight=1)
        self._root.columnconfigure(1, weight=2)

        # Resolution
        tk.Label(self._root, text='Resolution: ').grid(row=0, column=0, sticky='w')
        self._resolution_val = tk.StringVar()
        resolution = ttk.Combobox(self._root, textvariable=self._resolution_val)
        resolution['values'] = ('1920x1080', '1080x720', '720x480')
        resolution['state'] = 'readonly'
        resolution.current(1)
        resolution.grid(row=0, column=1, sticky='we')

        tk.Button(
            self._root, text="Run simulation", command=self._apply_settings
        ).grid(row=1, column=0, columnspan=2)

        # there are a few rows with 2 widgets and one with 1 widget
        for i in range((len(self._root.winfo_children()) + 1) // 2):
            self._root.rowconfigure(i, weight=1)

        for child in self._root.winfo_children():
            child.grid_configure(padx=10, pady=10)

        self._root.mainloop()

    def _apply_settings(self) -> None:
        res = self._resolution_val.get().split('x')
        self.screen_width: int = int(res[0])
        self.screen_height: int = int(res[1])

        self.screen_pond_width: int = self.screen_width
        # TODO: trzeba dobrac lepsza wartość
        self.screen_pond_height: int = int(self.screen_height * 0.9)
        self.screen_pond_height -= self.screen_pond_height % CELL_MIN_PX_SIZE

        self.pond_width: int = self.screen_pond_width // CELL_MIN_PX_SIZE
        self.pond_height: int = self.screen_pond_height // CELL_MIN_PX_SIZE

        self._root.destroy()
