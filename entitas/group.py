# -*- coding: utf-8 -*-

from .utils import Event
from .exceptions import GroupSingleEntity


class GroupEvent:
    added, removed, added_or_removed = range(3)


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
        self.entities = set()

    @property
    def single_entity(self):
        """Returns the only entity in this group.
        It will return None if the group is empty.
        It will throw a :class:`MissingComponent` if the group has more
        than one entity.
        """
        count = len(self.entities)

        if count == 1:
            return min(self.entities)
        if count == 0:
            return None

        raise GroupSingleEntity(
            'Cannot get a single entity from a group containing {} entities.',
            len(self.entities))

    def handle_entity_silently(self, entity):
        """This is used by the context to manage the group.
        :param matcher: Entity
        """
        if self._matcher.matches(entity):
            self._add_entity_silently(entity)
        else:
            self._remove_entity_silently(entity)

    def handle_entity(self, entity):
        """This is used by the context to manage the group.
        :param matcher: Entity
        """
        if self._matcher.matches(entity):
            self._add_entity(entity)
        else:
            self._remove_entity(entity)

    def update_entity(self, entity):
        """This is used by the context to manage the group.
        :param matcher: Entity
        """
        if entity in self.entities:
            self.on_entity_removed(entity)
            self.on_entity_added(entity)
            self.on_entity_updated(entity)

    def _add_entity_silently(self, entity):
        if entity not in self.entities:
            self.entities.add(entity)
            return True
        return False

    def _add_entity(self, entity):
        entity_added = self._add_entity_silently(entity)
        if entity_added:
            self.on_entity_added(entity)

    def _remove_entity_silently(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            return True
        return False

    def _remove_entity(self, entity):
        entity_removed = self._remove_entity_silently(entity)
        if entity_removed:
            self.on_entity_removed(entity)

    def __repr__(self):
        return '<Group [{}]>'.format(self._matcher)
