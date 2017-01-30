# -*- coding: utf-8 -*-

from .exceptions import (
    ExistingComponentException,
    MissingComponentException)


class Entity(object):
    """ An entity is a container holding data to represent certain
    objects in your application. You can add, replace or remove data
    from entities. Those containers are called 'components'.

    In entitas-python, a component is represented by a namedtuple
    because of readability.

    Usage::
      >>> import entitas
      >>> Position = namedtuple('Position', ['x', 'y', 'z'])
      >>> e = entitas.entity()
      >>> e.add(Position, [1, 2, 3])
      <Entity_0 [Position(x=1, y=2, z=3)]>
    """

    def __init__(self, creation_index=0):
        self._components = {}
        self.creation_index = creation_index

    @property
    def count(self):
        return len(self._components)

    def has(self, type):
        return type in self._components

    def get(self, type):
        if not self.has(type):
            raise MissingComponentException(
                'Cannot get unexisting component {0!r} from {1}.'
                .format(type.__name__, self))

        return self._components[type]

    def add(self, type, values):
        if self.has(type):
            raise ExistingComponentException(
                'Cannot add another component {0!r} to {1}.'
                .format(type.__name__, self))

        self._components[type] = type._make(values)

    def replace(self, type, values):
        self.remove(type)
        self.add(type, values)

    def remove(self, type):
        if not self.has(type):
            raise MissingComponentException(
                'Cannot remove unexisting component {0!r} from {1}.'
                .format(type.__name__, self))

        del self._components[type]

    def destroy(self):
        self._components.clear()

    def __repr__(self):
        return '<Entity_{i} [{c}]>'.format(
            i=self.creation_index,
            c=', '.join([str(self._components[x]) for x in self._components]))
