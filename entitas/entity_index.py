from abc import ABCMeta, abstractmethod

from .exceptions import EntitasException


class AbstractEntityIndex(metaclass=ABCMeta):

    def __init__(self, comp_type, group, *fields):
        self.type = comp_type
        self._group = group
        self._fields = fields
        self._index = {}
        self._activate()

    def __del__(self):
        self._deactivate()

    def _activate(self):
        self._group.on_entity_added += self._on_entity_added
        self._group.on_entity_removed += self._on_entity_removed
        self._index_entities()
        return self

    def _deactivate(self):
        self._group.on_entity_added -= self._on_entity_added
        self._group.on_entity_removed -= self._on_entity_removed
        self._index.clear()

    def _index_entities(self):
        for entity in self._group.entities:
            for field in self._fields:
                self._add_entity(getattr(entity.get(self.type), field), entity)

    def _on_entity_added(self, entity, component):
        for field in self._fields:
            self._add_entity(getattr(component, field), entity)

    def _on_entity_removed(self, entity, component):
        for field in self._fields:
            self._remove_entity(getattr(component, field), entity)

    @abstractmethod
    def _add_entity(self, key, entity):
        pass

    @abstractmethod
    def _remove_entity(self, key, entity):
        pass


class EntityIndex(AbstractEntityIndex):

    def get_entities(self, key):
        if key not in self._index:
            self._index[key] = set()
        return self._index[key]

    def _add_entity(self, key, entity):
        self.get_entities(key).add(entity)

    def _remove_entity(self, key, entity):
        self.get_entities(key).remove(entity)


class PrimaryEntityIndex(AbstractEntityIndex):

    def get_entity(self, key):
        return self._index[key]

    def _add_entity(self, key, entity):
        if key in self._index:
            raise EntitasException(
                "Entity for key '{key}' already exists!".format(key=key),
                "Only one entity for a primary key is allowed.")

        self._index[key] = entity

    def _remove_entity(self, key, entity):
        del self._index[key]
