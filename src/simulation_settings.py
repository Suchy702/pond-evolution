import traceback

import tkinter as tk
from tkinter import ttk

from src.constants import (
    CELL_MIN_PX_SIZE, SCREEN_DIMENSIONS, ALGA_ENERGY_VALUE, WORM_ENERGY_VALUE, ALGA_INTENSITY, WORM_INTENSITY
)


class SimulationSettings:
    def __init__(self):
        self._root: tk.Tk = None
        self._resolution_var: tk.StringVar = None
        self._fullscreen_var: tk.BooleanVar = None
        self._statistics_var: tk.BooleanVar = None

        self.fullscreen: bool = None
        self.statistics: bool = None

        self.speed_penalty: int = None
        self.size_penalty: int = None
        self.eyesight_penalty: int = None

        self.alga_energy: int = None
        self.worm_energy: int = None

        self.alga_intensity: int = None
        self.worm_intensity: int = None

        self.screen_width: int = None
        self.screen_height: int = None

        self.screen_pond_width: int = None
        self.screen_pond_height: int = None

        self.pond_width: int = None
        self.pond_height: int = None

        self.finished_setup: bool = False

    def _root_setup(self) -> None:
        self._root = tk.Tk()
        self._root.title("Settings")
        self._root.geometry("700x400")

    def _column_config(self) -> None:
        self._root.columnconfigure(0, weight=1)
        self._root.columnconfigure(1, weight=2)

    def _row_config(self) -> None:
        # There are a few rows with 2 widgets and two with 1 widget
        for i in range((len(self._root.winfo_children())) // 2 + 1):
            self._root.rowconfigure(i, weight=1)

    def _grid_config(self) -> None:
        for child in self._root.winfo_children():
            child.grid_configure(padx=10)

    def get_user_settings(self) -> None:
        self._root_setup()
        self._add_buttons()
        self._surface_configuration()
        self._root.mainloop()

    def _surface_configuration(self) -> None:
        self._column_config()
        self._row_config()
        self._grid_config()

    def _add_buttons(self) -> None:
        self._add_settings_buttons()
        self._add_error_prompt()
        self._add_run_simulation_button()

    def _add_settings_buttons(self) -> None:
        self._add_resolution_setting(0, 'Resolution')
        self._add_fullscreen_setting(1, 'Full screen mode')
        self._add_pond_size_setting(2, 'Pond size (width / height)')
        self._add_statistics_setting(3, 'Show statistics (it may take a while after simulation)')
        self._add_empty_pond_setting(4, 'Empty pond')
        self._add_no_worms_from_heaven_setting(5, 'No worms from heaven')
        self._add_no_alga_from_hell_setting(6, 'No alga from hell')
        self._add_traits_penalty_setting(7, 'Traits penalty (size / speed / eyesight)')
        self._add_energy_value_setting(8, 'Energy value (alga / worm)')
        self._add_intensity_setting(9, 'Intensity (alga / worm)')

    def _add_error_prompt(self) -> None:
        self._error_msg_var = tk.StringVar()
        tk.Label(self._root, fg='red', textvariable=self._error_msg_var).grid(row=10, column=0, columnspan=2)

    def _add_run_simulation_button(self) -> None:
        tk.Button(self._root, text="Run simulation", command=self._apply_settings).grid(row=11, column=0, columnspan=2)

    def _add_resolution_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._resolution_var = tk.StringVar()
        resolution = ttk.Combobox(self._root, textvariable=self._resolution_var)
        resolution.bind("<<ComboboxSelected>>", lambda _: self._update_resolution())
        resolution['values'] = SCREEN_DIMENSIONS
        resolution['state'] = 'readonly'
        resolution.current(1)
        resolution.grid(row=row, column=1, sticky='we')

    def _add_fullscreen_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')
        self._fullscreen_var = tk.BooleanVar()
        fullscreen = tk.Checkbutton(self._root, variable=self._fullscreen_var)
        fullscreen.grid(row=row, column=1, sticky='we')

    def _add_pond_size_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')

        spinbox_frame = tk.Frame(self._root)
        spinbox_frame.grid(row=row, column=1, sticky='nswe')

        spinbox_frame.rowconfigure(0, weight=1)

        for i in range(3):
            spinbox_frame.columnconfigure(i, weight=1)

        self._pond_width_var, self._pond_height_var = tk.StringVar(), tk.StringVar()
        pond_width = tk.Spinbox(spinbox_frame, from_=1, to=100, width=8, textvariable=self._pond_width_var)
        pond_height = tk.Spinbox(spinbox_frame, from_=1, to=100, width=8, textvariable=self._pond_height_var)
        pond_width.grid(row=0, column=0, sticky='w')
        pond_height.grid(row=0, column=2, sticky='e')

        self._update_resolution()

    def _add_traits_penalty_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')

        spinbox_frame = tk.Frame(self._root)
        spinbox_frame.grid(row=row, column=1, sticky='nswe')

        spinbox_frame.rowconfigure(0, weight=1)
        for i in range(5):
            spinbox_frame.columnconfigure(i, weight=1)

        self._speed_penalty_var, self._size_penalty_var, self._eyesight_penalty_var = \
            tk.StringVar(), tk.StringVar(), tk.StringVar()
        self._speed_penalty_var.set(value=str(100))
        self._size_penalty_var.set(value=str(100))
        self._eyesight_penalty_var.set(value=str(100))

        size_penalty = tk.Spinbox(spinbox_frame, from_=0, to=100, width=8, textvariable=self._size_penalty_var)
        speed_penalty = tk.Spinbox(spinbox_frame, from_=0, to=100, width=8, textvariable=self._speed_penalty_var)
        eyesight_penalty = tk.Spinbox(spinbox_frame, from_=0, to=100, width=8, textvariable=self._eyesight_penalty_var)

        size_penalty.grid(row=0, column=0, sticky='w')
        speed_penalty.grid(row=0, column=2)
        eyesight_penalty.grid(row=0, column=4, sticky='e')

        self._update_resolution()

    def _add_energy_value_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')

        spinbox_frame = tk.Frame(self._root)
        spinbox_frame.grid(row=row, column=1, sticky='nswe')

        spinbox_frame.rowconfigure(0, weight=1)

        for i in range(3):
            spinbox_frame.columnconfigure(i, weight=1)

        self._alga_energy_var, self._worm_energy_var = tk.StringVar(), tk.StringVar()
        self._alga_energy_var.set(value=str(ALGA_ENERGY_VALUE))
        self._worm_energy_var.set(value=str(WORM_ENERGY_VALUE))
        alga_energy = tk.Spinbox(spinbox_frame, from_=1, to=100, width=8, textvariable=self._alga_energy_var)
        worm_energy = tk.Spinbox(spinbox_frame, from_=1, to=100, width=8, textvariable=self._worm_energy_var)
        alga_energy.grid(row=0, column=0, sticky='w')
        worm_energy.grid(row=0, column=2, sticky='e')

    def _add_intensity_setting(self, row: int, text: str) -> None:
        tk.Label(self._root, text=f'{text}: ').grid(row=row, column=0, sticky='w')

        spinbox_frame = tk.Frame(self._root)
        spinbox_frame.grid(row=row, column=1, sticky='nswe')

        spinbox_frame.rowconfigure(0, weight=1)

        for i in range(3):
            spinbox_frame.columnconfigure(i, weight=1)

        self._alga_intensity_var, self._worm_intensity_var = tk.StringVar(), tk.StringVar()
        self._alga_intensity_var.set(value=str(ALGA_INTENSITY))
        self._worm_intensity_var.set(value=str(WORM_INTENSITY))
        alga_intensity = tk.Spinbox(spinbox_frame, from_=1, to=20, width=8, textvariable=self._alga_intensity_var)
        worm_intensity = tk.Spinbox(spinbox_frame, from_=1, to=20, width=8, textvariable=self._worm_intensity_var)
        alga_intensity.grid(row=0, column=0, sticky='w')
        worm_intensity.grid(row=0, column=2, sticky='e')

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

    def _apply_resolution(self) -> None:
        res = self._resolution_var.get().split('x')
        self.screen_width = int(res[0])
        self.screen_height = int(res[1])

        self._set_screen_dimensions()

    def _update_resolution(self) -> None:
        self._apply_resolution()
        self._pond_width_var.set(str(self.screen_pond_width // CELL_MIN_PX_SIZE))
        self._pond_height_var.set(str(self.screen_pond_height // CELL_MIN_PX_SIZE))

    def _get_user_choices(self) -> None:
        self.fullscreen = self._fullscreen_var.get()
        self.pond_width, self.pond_height = int(self._pond_width_var.get()), int(self._pond_height_var.get())
        self.statistics = self._statistics_var.get()
        self.empty_pond_setting = self._empty_pond_setting_var.get()
        self.no_worms_from_heaven = self._no_worms_from_heaven_var.get()
        self.no_alga_from_hell = self._no_alga_from_hell.get()
        self.speed_penalty = int(self._speed_penalty_var.get())
        self.size_penalty = int(self._size_penalty_var.get())
        self.eyesight_penalty = int(self._eyesight_penalty_var.get())
        self.alga_energy = int(self._alga_energy_var.get())
        self.worm_energy = int(self._worm_energy_var.get())
        self.alga_intensity = int(self._alga_intensity_var.get())
        self.worm_intensity = int(self._worm_intensity_var.get())

    def _set_screen_dimensions(self) -> None:
        self.screen_pond_width = self.screen_width
        self.screen_pond_height = int(self.screen_height * 0.9)
        self.screen_pond_height -= self.screen_pond_height % CELL_MIN_PX_SIZE

    def _validate_value_type(self) -> None:
        should_be_int = [
            self._pond_width_var.get(), self._pond_height_var.get(),
            self._speed_penalty_var.get(), self._size_penalty_var.get(), self._eyesight_penalty_var.get(),
            self._alga_energy_var.get(), self._worm_energy_var.get(),
            self._alga_intensity_var.get(), self._worm_intensity_var.get()
        ]

        for val in should_be_int:
            if not val.isdigit():
                raise TypeError("Values must be non-negative integer!")

    def _is_pond_dimensions_too_small(self) -> bool:
        too_small_height = self.pond_height < self.screen_pond_height // CELL_MIN_PX_SIZE
        too_small_widht = self.pond_width < self.screen_pond_width // CELL_MIN_PX_SIZE
        return too_small_height or too_small_widht

    def _is_pond_dimensions_too_big(self) -> bool:
        return self.pond_height > 200 or self.pond_width > 200

    def _exception_occurred(self, exception: Exception) -> None:
        print(traceback.format_exc())
        self._error_msg_var.set(str(exception))

    def _validate_pond_size(self) -> None:
        if self._is_pond_dimensions_too_small():
            min_width = self.screen_pond_width // CELL_MIN_PX_SIZE
            min_height = self.screen_pond_height // CELL_MIN_PX_SIZE
            raise ValueError(f'Pond size must be bigger than {min_width}x{min_height}!')

        if self._is_pond_dimensions_too_big():
            raise ValueError("Pond size must be smaller than 200x200!")

    def _is_traits_penalty_good(self) -> bool:
        min_good = 0 <= min(self.speed_penalty, self.size_penalty, self.eyesight_penalty)
        max_good = 200 >= max(self.speed_penalty, self.size_penalty, self.eyesight_penalty)
        return min_good and max_good

    def _validate_traits_penalty(self) -> None:
        if not self._is_traits_penalty_good():
            raise ValueError("Penalties must be in range [0, 200]!")

    def _is_energy_vals_good(self) -> bool:
        min_good = 0 <= min(self.alga_energy, self.worm_energy)
        max_good = 200 >= max(self.alga_energy, self.worm_energy)
        return min_good and max_good

    def _validate_energy(self) -> None:
        if not self._is_energy_vals_good():
            raise ValueError("Energy values must be in range [0, 200]!")

    def _is_intenisty_good(self) -> bool:
        min_good = 1 <= min(self.alga_intensity, self.worm_intensity)
        max_good = 20 >= max(self.alga_intensity, self.worm_intensity)
        return min_good and max_good

    def _validate_intensity(self) -> None:
        if not self._is_intenisty_good():
            raise ValueError("Intensity must be in range [1, 20]!")

    def _validate_data(self) -> None:
        self._validate_pond_size()
        self._validate_traits_penalty()
        self._validate_energy()
        self._validate_intensity()

    def _apply_settings(self) -> None:
        try:
            self._validate_value_type()
            self._get_user_choices()
            self._validate_data()
        except Exception as e:
            self._exception_occurred(e)
            return

        self.finished_setup = True
        self._root.destroy()
