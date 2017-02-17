# -*- coding: utf-8 -*-

from .group import GroupEvent


class Collector(object):

    def __init__(self):
        self._collected_entities = set()
        self._groups = {}

    @property
    def collected_entities(self):
        return list(self._collected_entities)

    def add(self, group, group_event):
        self._groups[group] = group_event

    def activate(self):
        for group in self._groups:
            group_event = self._groups[group]

            added_event = group_event == GroupEvent.added
            removed_event = group_event == GroupEvent.removed
            added_or_removed_event = group_event == GroupEvent.added_or_removed

            if added_event or added_or_removed_event:
                group.on_entity_added -= self._add_entity
                group.on_entity_added += self._add_entity

            if removed_event or added_or_removed_event:
                group.on_entity_removed -= self._add_entity
                group.on_entity_removed += self._add_entity

    def deactivate(self):
        for group in self._groups:
            group.on_entity_added -= self._add_entity
            group.on_entity_removed -= self._add_entity

        self.clear_collected_entities()

    def clear_collected_entities(self):
        self._collected_entities.clear()

    def _add_entity(self, entity, component):
        self._collected_entities.add(entity)

    def __repr__(self):
        return '<Collector [{}]'.format(
            ', '.join([str(group) for group in self._groups]))
