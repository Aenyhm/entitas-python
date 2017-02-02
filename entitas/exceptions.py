# -*- coding: utf-8 -*-

"""
entitas.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of Entitas' exceptions.
"""


class AlreadyAddedComponent(Exception):
    """The entity already contains this type of component."""


class MissingComponent(Exception):
    """The entity does not contain this type of component."""


class MissingEntity(Exception):
    """The context does not contain this entity."""


class GroupSingleEntity(Exception):
    """The group contains more than one entity."""
