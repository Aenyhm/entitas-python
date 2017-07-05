from enum import Enum

from .utils import Event
from .exceptions import GroupSingleEntity


class GroupEvent(Enum):
    ADDED = 1
    REMOVED = 2
    ADDED_OR_REMOVED = 3


class Group(object):
    """Use context.get_group(matcher) to get a group of entities which
    match the specified matcher. Calling context.get_group(matcher) with
    the same matcher will always return the same instance of the group.

    The created group is managed by the context and will always be up to
    date. It will automatically add entities that match the matcher or
    remove entities as soon as they don't match the matcher anymore.
    """

    def __init__(self, matcher):

        #: Occurs when an entity gets added.
        self.on_entity_added = Event()

        #: Occurs when an entity gets removed.
        self.on_entity_removed = Event()

        #: Occurs when a component of an entity in the group gets
        # replaced.
        self.on_entity_updated = Event()

        self._matcher = matcher
        self._entities = set()

    @property
    def entities(self):
        return self._entities

    @property
    def single_entity(self):
        """Returns the only entity in this group.
        It will return None if the group is empty.
        It will throw a :class:`MissingComponent` if the group has more
        than one entity.
        """
        count = len(self._entities)

        if count == 1:
            return min(self._entities)
        if count == 0:
            return None

        raise GroupSingleEntity(
            'Cannot get a single entity from a group containing {} entities.',
            len(self._entities))

    def handle_entity_silently(self, entity):
        """This is used by the context to manage the group.
        :param matcher: Entity
        """
        if self._matcher.matches(entity):
            self._add_entity_silently(entity)
        else:
            self._remove_entity_silently(entity)

    def handle_entity(self, entity, component):
        """This is used by the context to manage the group.
        :param matcher: Entity
        """
        if self._matcher.matches(entity):
            self._add_entity(entity, component)
        else:
            self._remove_entity(entity, component)

    def update_entity(self, entity, previous_comp, new_comp):
        """This is used by the context to manage the group.
        :param matcher: Entity
        """
        if entity in self._entities:
            self.on_entity_removed(entity, previous_comp)
            self.on_entity_added(entity, new_comp)
            self.on_entity_updated(entity, previous_comp, new_comp)

    def _add_entity_silently(self, entity):
        if entity not in self._entities:
            self._entities.add(entity)
            return True
        return False

    def _add_entity(self, entity, component):
        entity_added = self._add_entity_silently(entity)
        if entity_added:
            self.on_entity_added(entity, component)

    def _remove_entity_silently(self, entity):
        if entity in self._entities:
            self._entities.remove(entity)
            return True
        return False

    def _remove_entity(self, entity, component):
        entity_removed = self._remove_entity_silently(entity)
        if entity_removed:
            self.on_entity_removed(entity, component)

    def __repr__(self):
        return '<Group [{}]>'.format(self._matcher)
