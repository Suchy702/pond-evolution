from typing import cast

import pandas as pd

from src.logic.engine import Engine
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings


class Statistics:
    def __init__(self, settings: SimulationSettings, engine: Engine):
        self._settings = settings
        self._engine = engine

        self._dataframe: pd.DataFrame = pd.DataFrame(
            columns=['cycle', 'size', 'speed', 'eyesight', 'type', 'is_smart']
        )
        dtypes = {
            'cycle': 'int32', 'size': 'int32', 'speed': 'int32', 'eyesight': 'int32', 'type': 'category',
            'is_smart': 'bool'
        }
        self._dataframe = self._dataframe.astype(dtypes)

    def make_snapshot(self) -> None:
        if not self._settings.statistics:
            return

        fish_list = self._engine.objects_by_type(ObjectKind.FISH)
        fish_list = cast(list[Fish], fish_list)

        for fish in fish_list:
            self._add_record(fish)

    def _add_record(self, fish: Fish) -> None:
        data = [
            self._engine.cycle_count - 1, fish.size, fish.speed, fish.eyesight,
            'predator' if FishTrait.PREDATOR in fish.traits else fish.fish_type.name.lower(),
            FishTrait.SMART in fish.traits
        ]
        self._dataframe.loc[self._dataframe.shape[0]] = data

    def show_statistics(self) -> None:
        if self._settings.statistics:
            print(self._dataframe)
