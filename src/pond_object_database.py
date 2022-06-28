from src.pond_object import PondObject


class PondObjectDatabase:
    def __init__(self):
        self._base: dict[int, PondObject] = {}
        self._id_counter: int = 0

    @property
    def objects(self):
        return list(self._base.values())

    @property
    def size(self):
        return len(self._base)

    def add(self, obj: PondObject) -> None:
        if obj.id in self._base:
            raise Exception("Object already in base!")
        self._id_counter += 1
        obj.set_id(self._id_counter)
        self._base[obj.id] = obj

    def remove(self, obj: PondObject) -> None:
        if obj.id not in self._base:
            raise Exception("Object not in base!")
        self._base.pop(obj.id)
