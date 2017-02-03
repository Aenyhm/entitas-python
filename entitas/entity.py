# -*- coding: utf-8 -*-

from .utils import Event
from .exceptions import AlreadyAddedComponent, MissingComponent


class Entity(object):
    """ An entity is a container holding data to represent certain
    objects in your application. You can add, replace or remove data
    from entities.

    Those containers are called 'components'. They are represented by
    namedtuples for readability.
    """

    def __init__(self):

        #: Dictionary mapping component type and component instance.
        self._components = {}

        #: Entities unique identifier per context.
        self.creation_index = 0

        self.on_component_added = Event()
        self.on_component_removed = Event()
        self.on_component_replaced = Event()

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

    def add(self, comp_type, *args):
        self._add_silently(comp_type, *args)
        self.on_component_added(self)

    def remove(self, comp_type):
        self._remove_silently(comp_type)
        self.on_component_removed(self)

    def replace(self, comp_type, *args):
        """As namedtuples are immutable, simply remove the existing
        component then add a new one with the given values.
        :param comp_type: namedtuple type
        :param *args: (optional) data values
        """
        self._remove_silently(comp_type)
        self._add_silently(comp_type, *args)
        self.on_component_replaced(self)

    def destroy(self):
        """Removes all components."""
        self._components.clear()

    def _add_silently(self, comp_type, *args):
        """Adds a component. If the entity already contains a component
        of its type, a :class:`AlreadyAddedComponent` exception is
        raised.
        :param comp_type: namedtuple type
        :param *args: (optional) data values
        """
        if self.has(comp_type):
            raise AlreadyAddedComponent(
                'Cannot add another component {!r} to {}.'
                .format(comp_type.__name__, self))

        self._components[comp_type] = comp_type._make(args)

    def _remove_silently(self, comp_type):
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

    def __repr__(self):
        """ <Entity_0 [Position(x=1, y=2, z=3)]> """
        return '<Entity_{} [{}]>'.format(
            self.creation_index,
            ', '.join([str(self._components[x]) for x in self._components]))
