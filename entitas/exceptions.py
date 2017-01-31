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
