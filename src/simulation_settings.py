import tkinter as tk
from tkinter import ttk

from src.constants import CELL_MIN_PX_SIZE, SCREEN_DIMENSIONS


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

    def _root_setup(self) -> None:
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.geometry("550x250")

    def _column_config(self) -> None:
        self._root.columnconfigure(0, weight=1)
        self._root.columnconfigure(1, weight=2)

    def _add_settings_buttons(self) -> None:
        self._add_resolution_setting(0, 'Resolution')
        self._add_fullscreen_setting(1, 'Full screen mode')
        self._add_statistics_setting(2, 'Show statistics (it may take a while after simulation)')
        self._add_empty_pond_setting(3, 'Empty pond')
        self._add_no_worms_from_heaven_setting(4, 'No worms from heaven')
        self._add_no_alga_from_hell_setting(5, 'No alga from hell')

    def _add_run_simulation_button(self) -> None:
        tk.Button(self._root, text="Run simulation", command=self._apply_settings).grid(row=6, column=0, columnspan=2)

    def _row_config(self) -> None:
        # There are a few rows with 2 widgets and one with 1 widget
        for i in range((len(self._root.winfo_children()) + 1) // 2):
            self._root.rowconfigure(i, weight=1)

    def _grid_config(self) -> None:
        for child in self._root.winfo_children():
            child.grid_configure(padx=10)

    def _surface_configuration(self) -> None:
        self._column_config()
        self._row_config()
        self._grid_config()

    def _add_buttons(self) -> None:
        self._add_settings_buttons()
        self._add_run_simulation_button()

    def get_user_settings(self) -> None:
        self._root_setup()
        self._add_buttons()
        self._surface_configuration()
        self._root.mainloop()

    def _add_resolution_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._resolution_var = tk.StringVar()
        resolution = ttk.Combobox(self._root, textvariable=self._resolution_var)
        resolution['values'] = SCREEN_DIMENSIONS
        resolution['state'] = 'readonly'
        resolution.current(1)
        resolution.grid(row=row, column=1, sticky='we')

    def _add_fullscreen_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._fullscreen_var = tk.BooleanVar()
        fullscreen = tk.Checkbutton(self._root, variable=self._fullscreen_var)
        fullscreen.grid(row=row, column=1, sticky='we')

    def _add_statistics_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._statistics_var = tk.BooleanVar()
        statistics = tk.Checkbutton(self._root, variable=self._statistics_var)
        statistics.grid(row=row, column=1, sticky='we')

    def _add_empty_pond_setting(self, row, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._empty_pond_setting_var = tk.BooleanVar()
        empty_pond_setting = tk.Checkbutton(self._root, variable=self._empty_pond_setting_var)
        empty_pond_setting.grid(row=row, column=1, sticky='we')

    def _add_no_worms_from_heaven_setting(self, row, text) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._no_worms_from_heaven_var = tk.BooleanVar()
        no_worms_from_heaven = tk.Checkbutton(self._root, variable=self._no_worms_from_heaven_var)
        no_worms_from_heaven.grid(row=row, column=1, sticky='we')

    def _add_no_alga_from_hell_setting(self, row, text) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._no_alga_from_hell = tk.BooleanVar()
        no_alga_from_hell = tk.Checkbutton(self._root, variable=self._no_alga_from_hell)
        no_alga_from_hell.grid(row=row, column=1, sticky='we')

    def _resolution_apply(self) -> None:
        res = self._resolution_var.get().split('x')
        self.screen_width = int(res[0])
        self.screen_height = int(res[1])

    def _get_user_choices(self) -> None:
        self.fullscreen = self._fullscreen_var.get()
        self.statistics = self._statistics_var.get()
        self.empty_pond_setting = self._empty_pond_setting_var.get()
        self.no_worms_from_heaven = self._no_worms_from_heaven_var.get()
        self.no_alga_from_hell = self._no_alga_from_hell.get()

    def _set_screen_dimensions(self) -> None:
        self.screen_pond_width = self.screen_width
        self.screen_pond_height = int(self.screen_height * 0.9)
        self.screen_pond_height -= self.screen_pond_height % CELL_MIN_PX_SIZE

    def _set_pond_dimensions(self) -> None:
        self.pond_width = self.screen_pond_width // CELL_MIN_PX_SIZE
        self.pond_height = self.screen_pond_height // CELL_MIN_PX_SIZE

    def _set_dimensions(self) -> None:
        self._set_screen_dimensions()
        self._set_pond_dimensions()

    def _apply_settings(self) -> None:
        self._resolution_apply()
        self._get_user_choices()
        self._set_dimensions()
        self._root.destroy()
