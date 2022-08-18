from src.object.pond_object import PondObject


class PondObjectDatabase:
    def __init__(self):
        self._object_database: dict[int, PondObject] = {}
        self._id_counter: int = 0

    @property
    def objects(self) -> list[PondObject]:
        return list(self._object_database.values())

    @property
    def size(self) -> int:
        return len(self._object_database)

    def add(self, object_: PondObject) -> None:
        if object_.id in self._object_database:
            raise Exception("Object already in database!")

        self._id_counter += 1
        object_.id = self._id_counter
        self._object_database[object_.id] = object_

    def remove(self, object_: PondObject) -> None:
        if object_.id not in self._object_database:
            raise Exception("Object not in database!")

        self._object_database.pop(object_.id)
