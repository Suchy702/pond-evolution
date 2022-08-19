from __future__ import annotations

from typing import cast, TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.logic.engine import Engine
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.object_kind import ObjectKind

if TYPE_CHECKING:
    from src.simulation_settings import SimulationSettings

sns.set_theme(style="darkgrid")


class Statistics:
    def __init__(self, settings: SimulationSettings, engine: Engine):
        self._settings = settings
        self._engine = engine

        self._raw_data: list[list] = []
        self._dataframe: pd.DataFrame = None
        self._plot_idx = 0

    def make_snapshot(self) -> None:
        if not self._settings.statistics:
            return

        fish_list = self._engine.objects_by_type(ObjectKind.FISH)
        fish_list = cast(list[Fish], fish_list)

        for fish in fish_list:
            self._add_record(fish)

    def show_statistics(self) -> None:
        if not self._settings.statistics:
            return

        self._dataframe = pd.DataFrame(
            self._raw_data,
            columns=['cycle', 'size', 'speed', 'eyesight', 'type', 'is_smart']
        )
        dtypes = {
            'cycle': 'int32', 'size': 'int32', 'speed': 'int32', 'eyesight': 'int32', 'type': 'category',
            'is_smart': 'bool'
        }

        self._dataframe = self._dataframe.astype(dtypes)
        self._draw_plot()

    def _add_record(self, fish: Fish) -> None:
        data = [
            self._engine.cycle_count - 1, fish.size, fish.speed, fish.eyesight,
            'predator' if FishTrait.PREDATOR in fish.traits else fish.fish_type.name.lower(),
            FishTrait.SMART in fish.traits
        ]
        self._raw_data.append(data)

    def _draw_plot(self) -> None:
        self._draw_population_plot()
        self._draw_traits_plot()

        plt.tight_layout()
        plt.show(block=True)

    def _draw_population_plot(self) -> None:
        df = self._dataframe[['cycle', 'type', 'speed']].rename(columns={'speed': 'count'})
        df = df.groupby(['cycle', 'type']).count().astype('int32').reset_index()

        sns.relplot(x='cycle', y='count', hue='type', kind='line', ci=None, data=df)

    def _draw_traits_plot(self) -> None:
        df = self._dataframe.melt(id_vars=['cycle', 'type'], value_vars=['size', 'speed', 'eyesight'])
        sns.displot(df, x='cycle', y='value', col='type', row='variable', cbar=True)
