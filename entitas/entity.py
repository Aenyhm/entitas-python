# -*- coding: utf-8 -*-

"""
entitas.entity
~~~~~~~~~~~~~~

This module contains the Entity class.
"""
from .exceptions import AlreadyAddedComponent, MissingComponent


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
      >>> e.replace(Position, [4, 5, 6])
      <Entity_0 [Position(x=4, y=5, z=6)]>
      >>> e.remove(Position)
      <Entity_0 []>
    """

    def __init__(self):

        #: Dictionary mapping component type and component instance.
        self._components = {}

        #: Entities differenciation.
        self.creation_index = 0

    @property
    def count(self):
        """Returns the number of components.
        :rtype: int
        """
        return len(self._components)

    def has(self, key):
        """Checks if the entity has a component of this type.
        :param key: :type: namedtuple type
        :rtype: bool
        """
        return key in self._components

    def get(self, key):
        """Retrieves a component by its type. If it does not exist,
        a :class:`MissingComponent` exception is raised.
        :param key: :type: namedtuple type
        :rtype: namedtuple
        """
        if not self.has(key):
            raise MissingComponent(
                'Cannot get unexisting component {!r} from {}.'
                .format(key.__name__, self))

        return self._components[key]

    def add(self, key, values):
        """Adds a component. If the entity already contains a component
        of its type, a :class:`AlreadyAddedComponent` exception is
        raised.
        :param key: :type: namedtuple type
        :param values: :list: component data
        """
        if self.has(key):
            raise AlreadyAddedComponent(
                'Cannot add another component {!r} to {}.'
                .format(key.__name__, self))

        self._components[key] = key._make(values)

    def replace(self, key, values):
        """As namedtuples are immutable, simply remove the existing
        component then add a new one with the given values.
        :param key: :type: namedtuple type
        :param values: :list: component data
        """
        self.remove(key)
        self.add(key, values)

    def remove(self, key):
        """Removes a component. If the entity does not contain a
        component of its type, a :class:`MissingComponent` exception is
        raised.
        :param key: :type: namedtuple type
        """
        if not self.has(key):
            raise MissingComponent(
                'Cannot remove unexisting component {!r} from {}.'
                .format(key.__name__, self))

        del self._components[key]

    def destroy(self):
        """Removes all components."""
        self._components.clear()

    def __repr__(self):
        """ <Entity_0 [Position(x=1, y=2, z=3)]> """
        return '<Entity_{} [{}]>'.format(
            self.creation_index,
            ', '.join([str(self._components[x]) for x in self._components]))
