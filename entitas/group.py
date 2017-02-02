# -*- coding: utf-8 -*-

from .exceptions import GroupSingleEntity


class Group(object):

    def __init__(self, matcher):
        self._matcher = matcher
        self.entities = set()

    def handle_entity(self, entity):
        if self._matcher.matches(entity):
            self.entities.add(entity)
        else:
            self.entities.remove(entity)

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
