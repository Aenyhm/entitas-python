# -*- coding: utf-8 -*-

"""
entitas.core
~~~~~~~~~~~~

This module contains the ECS features.

Usage::
  >>> import entitas
  >>> Position = namedtuple('Position', ['x', 'y', 'z'])
  >>> context = entitas.Context()
  >>> entity = context.create_entity()
  >>> entity.add(Position, [1, 2, 3])
  <Entity_0 [Position(x=1, y=2, z=3)]>
  >>> entity.replace(Position, [4, 5, 6])
  <Entity_0 [Position(x=4, y=5, z=6)]>
  >>> entity.remove(Position)
  <Entity_0 []>
"""
from collections import deque

from .exceptions import (
    AlreadyAddedComponent, MissingComponent, MissingEntity)


class Entity(object):
    """ An entity is a container holding data to represent certain
    objects in your application. You can add, replace or remove data
    from entities. Those containers are called 'components'.

    In entitas-python, a component is represented by a namedtuple
    because of readability.
    """

    def __init__(self):

        #: Dictionary mapping component type and component instance.
        self._components = {}

        #: Entities unique identifier per context.
        self.creation_index = 0

    @property
    def count(self):
        """Returns the number of components.
        :rtype: int
        """
        return len(self._components)

    def has(self, *args):
        """Checks if the entity has all components of the given type(s).
        :param args: namedtuple types
        :rtype: bool
        """
        return all([comp_type in self._components for comp_type in args])

    def has_any(self, *args):
        """Checks if the entity has any component of the given type(s).
        :param args: namedtuple types
        :rtype: bool
        """
        return any([comp_type in self._components for comp_type in args])

    def get(self, comp_type):
        """Retrieves a component by its type. If it does not exist,
        a :class:`MissingComponent` exception is raised.
        :param comp_type: namedtuple type
        :rtype: namedtuple
        """
        if not self.has(comp_type):
            raise MissingComponent(
                'Cannot get unexisting component {!r} from {}.'
                .format(comp_type.__name__, self))

        return self._components[comp_type]

    def add(self, comp_type, data):
        """Adds a component. If the entity already contains a component
        of its type, a :class:`AlreadyAddedComponent` exception is
        raised.
        :param comp_type: namedtuple type
        :param data: list of values
        """
        if self.has(comp_type):
            raise AlreadyAddedComponent(
                'Cannot add another component {!r} to {}.'
                .format(comp_type.__name__, self))

        self._components[comp_type] = comp_type._make(data)

    def replace(self, comp_type, data):
        """As namedtuples are immutable, simply remove the existing
        component then add a new one with the given values.
        :param comp_type: namedtuple type
        :param data: list of values
        """
        self.remove(comp_type)
        self.add(comp_type, data)

    def remove(self, comp_type):
        """Removes a component. If the entity does not contain a
        component of its type, a :class:`MissingComponent` exception is
        raised.
        :param comp_type: namedtuple type
        """
        if not self.has(comp_type):
            raise MissingComponent(
                'Cannot remove unexisting component {!r} from {}.'
                .format(comp_type.__name__, self))

        del self._components[comp_type]

    def destroy(self):
        """Removes all components."""
        self._components.clear()

    def __repr__(self):
        """ <Entity_0 [Position(x=1, y=2, z=3)]> """
        return '<Entity_{} [{}]>'.format(
            self.creation_index,
            ', '.join([str(self._components[x]) for x in self._components]))


class Context(object):
    """ A context is a data structure managing entities, i. e. creation,
    destruction, iteration & search.
    """

    def __init__(self):

        #: Entities retained by this context.
        self._entities = []

        #: An object pool to recycle entities.
        self._reusable_entities = deque()

        #: Entities counter.
        self._entity_index = 0

    @property
    def count(self):
        """Returns the number of retained entities.
        :rtype: int
        """
        return len(self._entities)

    def has(self, entity):
        """Checks if the context contains this entity.
        :param entity: entitas.Entity
        :rtype: bool
        """
        return entity in self._entities

    def create_entity(self):
        """Creates an entity. Pop one entity from the pool if it is not
        empty, otherwise creates a new one. Increments the entity index.
        Then adds the entity to the list.
        :rtype: entitas.Entity
        """
        entity = (self._reusable_entities.pop()
                  if len(self._reusable_entities) > 0
                  else Entity())

        entity.creation_index = self._entity_index
        self._entity_index += 1

        self._entities.append(entity)
        return entity

    def destroy(self, entity):
        """Removes an entity from the list and add it to the pool. If
        the context does not contain this entity, a
        :class:`MissingEntity` exception is raised.
        :param entity: entitas.Entity
        """
        if not self.has(entity):
            raise MissingEntity()

        self._entities.remove(entity)
        self._reusable_entities.append(entity)

    def __repr__(self):
        """ <Context (2/5)> """
        return '<Context ({}/{})>'.format(
            self.count, len(self._reusable_entities))
