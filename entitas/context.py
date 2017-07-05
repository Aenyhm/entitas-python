from collections import deque

from .entity import Entity
from .matcher import Matcher
from .group import Group
from .exceptions import MissingEntity


class Context(object):
    """A context is a data structure managing entities."""

    def __init__(self):

        #: Entities retained by this context.
        self._entities = set()

        #: An object pool to recycle entities.
        self._reusable_entities = deque()

        #: Entities counter.
        self._entity_index = 0

        #: Dictionary of matchers mapping groups.
        self._groups = {}

        self._entity_indices = {}

    @property
    def entities(self):
        return self._entities

    def has_entity(self, entity):
        """Checks if the context contains this entity.
        :param entity: Entity
        :rtype: bool
        """
        return entity in self._entities

    def create_entity(self):
        """Creates an entity. Pop one entity from the pool if it is not
        empty, otherwise creates a new one. Increments the entity index.
        Then adds the entity to the list.
        :rtype: Entity
        """
        entity = (self._reusable_entities.pop() if self._reusable_entities
                  else Entity())

        entity.activate(self._entity_index)
        self._entity_index += 1

        self._entities.add(entity)

        entity.on_component_added += self._comp_added_or_removed
        entity.on_component_removed += self._comp_added_or_removed
        entity.on_component_replaced += self._comp_replaced

        return entity

    def destroy_entity(self, entity):
        """Removes an entity from the list and add it to the pool. If
        the context does not contain this entity, a
        :class:`MissingEntity` exception is raised.
        :param entity: Entity
        """
        if not self.has_entity(entity):
            raise MissingEntity()

        entity.destroy()

        self._entities.remove(entity)
        self._reusable_entities.append(entity)

    def get_group(self, matcher):
        """User can ask for a group of entities from the context. The
        group is identified through a :class:`Matcher`.
        :param entity: Matcher
        """
        if matcher in self._groups:
            return self._groups[matcher]

        group = Group(matcher)

        for entity in self._entities:
            group.handle_entity_silently(entity)

        self._groups[matcher] = group

        return group

    def set_unique_component(self, comp_type, *args):
        self.create_entity().add(comp_type, *args)

    def get_unique_component(self, comp_type):
        group = self.get_group(Matcher(comp_type))
        return group.single_entity.get(comp_type)

    def add_entity_index(self, entity_index):
        self._entity_indices[entity_index.type] = entity_index

    def get_entity_index(self, comp_type):
        return self._entity_indices[comp_type]

    def _comp_added_or_removed(self, entity, comp):
        for matcher in self._groups:
            self._groups[matcher].handle_entity(entity, comp)

    def _comp_replaced(self, entity, previous_comp, new_comp):
        for matcher in self._groups:
            group = self._groups[matcher]
            group.update_entity(entity, previous_comp, new_comp)

    def __repr__(self):
        return '<Context ({}/{})>'.format(
            len(self._entities), len(self._reusable_entities))
