"""
entitas.entity
~~~~~~~~~~~~~~
An entity is a container holding data to represent certain
objects in your application. You can add, replace or remove data
from entities.

Those containers are called 'components'. They are represented by
namedtuples for readability.
"""

from .utils import Event
from .exceptions import (
    EntityNotEnabled, AlreadyAddedComponent, MissingComponent)


class Entity(object):
    """Use context.create_entity() to create a new entity and
    context.destroy_entity() to destroy it.
    You can add, replace and remove components to an entity.
    """

    def __init__(self):

        #: Occurs when a component gets added.
        self.on_component_added = Event()

        #: Occurs when a component gets removed.
        self.on_component_removed = Event()

        #: Occurs when a component gets replaced.
        self.on_component_replaced = Event()

        #: Dictionary mapping component type and component instance.
        self._components = {}

        #: Each entity has its own unique creationIndex which will be
        #: set by the context when you create the entity.
        self._creation_index = 0

        #: The context manages the state of an entity.
        #: Active entities are enabled, destroyed entities are not.
        self._is_enabled = False

    def activate(self, creation_index):
        self._creation_index = creation_index
        self._is_enabled = True

    def add(self, comp_type, *args):
        """Adds a component.
        :param comp_type: namedtuple type
        :param *args: (optional) data values
        """
        if not self._is_enabled:
            raise EntityNotEnabled(
                'Cannot add component {!r}: {} is not enabled.'
                .format(comp_type.__name__, self))

        if self.has(comp_type):
            raise AlreadyAddedComponent(
                'Cannot add another component {!r} to {}.'
                .format(comp_type.__name__, self))

        new_comp = comp_type._make(args)
        self._components[comp_type] = new_comp
        self.on_component_added(self, new_comp)

    def remove(self, comp_type):
        """Removes a component.
        :param comp_type: namedtuple type
        """
        if not self._is_enabled:
            raise EntityNotEnabled(
                'Cannot remove component {!r}: {} is not enabled.'
                .format(comp_type.__name__, self))

        if not self.has(comp_type):
            raise MissingComponent(
                'Cannot remove unexisting component {!r} from {}.'
                .format(comp_type.__name__, self))

        self._replace(comp_type, None)

    def replace(self, comp_type, *args):
        """Replaces an existing component or adds it if it doesn't exist
        yet.
        :param comp_type: namedtuple type
        :param *args: (optional) data values
        """
        if not self._is_enabled:
            raise EntityNotEnabled(
                'Cannot replace component {!r}: {} is not enabled.'
                .format(comp_type.__name__, self))

        if self.has(comp_type):
            self._replace(comp_type, args)
        else:
            self.add(comp_type, *args)

    def _replace(self, comp_type, args):
        previous_comp = self._components[comp_type]
        if args is None:
            del self._components[comp_type]
            self.on_component_removed(self, previous_comp)
        else:
            new_comp = comp_type._make(args)
            self._components[comp_type] = new_comp
            self.on_component_replaced(self, previous_comp, new_comp)

    def get(self, comp_type):
        """Retrieves a component by its type.
        :param comp_type: namedtuple type
        :rtype: namedtuple
        """
        if not self.has(comp_type):
            raise MissingComponent(
                'Cannot get unexisting component {!r} from {}.'
                .format(comp_type.__name__, self))

        return self._components[comp_type]

    def has(self, *args):
        """Checks if the entity has all components of the given type(s).
        :param args: namedtuple types
        :rtype: bool
        """
        if len(args) == 1:
            return args[0] in self._components

        return all([comp_type in self._components for comp_type in args])

    def has_any(self, *args):
        """Checks if the entity has any component of the given type(s).
        :param args: namedtuple types
        :rtype: bool
        """
        return any([comp_type in self._components for comp_type in args])

    def remove_all(self):
        """Removes all components."""
        for comp_type in list(self._components):
            self._replace(comp_type, None)

    def destroy(self):
        """This method is used internally. Don't call it yourself.
        Use context.destroy_entity(entity).
        """
        self._is_enabled = False
        self.remove_all()

    def __repr__(self):
        """ <Entity_0 [Position(x=1, y=2, z=3)]> """
        return '<Entity_{} [{}]>'.format(
            self._creation_index,
            ', '.join([str(self._components[x]) for x in self._components]))
