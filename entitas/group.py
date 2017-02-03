# -*- coding: utf-8 -*-

from .utils import Event
from .exceptions import GroupSingleEntity


class Group(object):

    def __init__(self, matcher):
        self._matcher = matcher
        self.entities = set()
        self.on_entity_added = Event()
        self.on_entity_removed = Event()
        self.on_entity_added_or_removed = Event()

    @property
    def single_entity(self):
        count = len(self.entities)

        if count == 1:
            return min(self.entities)
        if count == 0:
            return None

        raise GroupSingleEntity(
            'Cannot get a single entity from a group containing {} entities.',
            len(self.entities))

    def handle_entity(self, entity, silently):
        if self._matcher.matches(entity):
            if entity not in self.entities:
                self.entities.add(entity)
                if not silently:
                    self.on_entity_added(entity)
                    self.on_entity_added_or_removed(entity)
        else:
            if entity in self.entities:
                self.entities.remove(entity)
                if not silently:
                    self.on_entity_removed(entity)
                    self.on_entity_added_or_removed(entity)

    def update_entity(self, entity):
        self.on_entity_added_or_removed(entity)
