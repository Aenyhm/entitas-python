# -*- coding: utf-8 -*-

from collections import deque

from .entity import Entity
from .group import Group
from .exceptions import MissingEntity


class Context(object):
    """A context is a data structure managing entities."""

    def __init__(self):

        #: Entities retained by this context.
        self.entities = set()

        #: An object pool to recycle entities.
        self._reusable_entities = deque()

        #: Entities counter.
        self._entity_index = 0

        #: Dictionary of matchers mapping groups.
        self._groups = {}

    @property
    def count(self):
        """Returns the number of retained entities.
        :rtype: int
        """
        return len(self.entities)

    def has_entity(self, entity):
        """Checks if the context contains this entity.
        :param entity: Entity
        :rtype: bool
        """
        return entity in self.entities

    def create_entity(self):
        """Creates an entity. Pop one entity from the pool if it is not
        empty, otherwise creates a new one. Increments the entity index.
        Then adds the entity to the list.
        :rtype: Entity
        """
        entity = (self._reusable_entities.pop()
                  if len(self._reusable_entities) > 0
                  else Entity())

        entity.activate(self._entity_index)
        self._entity_index += 1

        self.entities.add(entity)

        entity.on_component_added += self._comp_added_or_removed
        entity.on_component_removed += self._comp_added_or_removed
        entity.on_component_replaced += self._comp_replaced

        return entity

    def destroy_entity(self, entity):
        """Removes an entity from the list and add it to the pool. If
        the context does not contain this entity, a
        :class:`MissingEntity` exception is raised.
        :param entity: entitas.Entity
        """
        if not self.has_entity(entity):
            raise MissingEntity()

        entity.destroy()

        self.entities.remove(entity)
        self._reusable_entities.append(entity)

    def get_group(self, matcher):
        """User can ask for a group of entities from the context. The
        group is identified through a :class:`Matcher`.
        """
        if matcher in self._groups:
            return self._groups[matcher]

        group = Group(matcher)

        for entity in self.entities:
            group.handle_entity_silently(entity)

        self._groups[matcher] = group

        return group

    def _comp_added_or_removed(self, entity):
        for matcher in self._groups:
            self._groups[matcher].handle_entity(entity)

    def _comp_replaced(self, entity):
        for matcher in self._groups:
            self._groups[matcher].update_entity(entity)

    def __repr__(self):
        return '<Context ({}/{})>'.format(
            self.count, len(self._reusable_entities))