from object import Object, Group, GroupNames


class Item(Object):
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self._name = name
        if GroupNames.item not in Item.groups.keys():
            Item.groups[GroupNames.item] = Group(GroupNames.item)
        Item.groups[GroupNames.item].add(self)

    def die(self):
        Item.groups[GroupNames.item].remove(self)
        super().die()

    @property
    def name(self):
        return self._name

