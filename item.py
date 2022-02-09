from object import Object


class Item(Object):
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self._name = name

    @property
    def name(self):
        return self._name
