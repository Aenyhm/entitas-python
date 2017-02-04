# -*- coding: utf-8 -*-

"""
Entitas for Python
~~~~~~~~~~~~~~~~~~

entitas-python is a port of Entitas-CSharp, a popular ECS.

:copyright: (c) 2017 by Fabien Nouaillat.
:license: MIT, see LICENSE for more details.
"""

from .entity import Entity
from .context import Context
from .matcher import Matcher
from .group import Group
from .processors import Processors
from .utils import Event
from .exceptions import (
    AlreadyAddedComponent, MissingComponent,
    MissingEntity, GroupSingleEntity)


__title__ = 'Entitas'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Fabien Nouaillat'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Fabien Nouaillat'
